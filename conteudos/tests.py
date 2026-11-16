from django.contrib.auth.models import Group, User
from django.test import TestCase
from django.urls import reverse

from usuarios.models import Usuario
from .models import CanalApoio, ConteudoEducativo

SENHA = 'senha-forte-123'


class ConteudoTest(TestCase):
    def setUp(self):
        self.cae = User.objects.create_user(
            'cae1', password=SENHA, first_name='Marina', last_name='Souza',
        )
        self.cae.groups.add(Group.objects.get(name='CAE'))

        self.ana = Usuario(username='ana', cpf='111.111.111-11', rg='1111', endereco='Rua A')
        self.ana.set_password(SENHA)
        self.ana.save()
        self.ana.groups.add(Group.objects.get(name='Denunciante'))

        self.canal = CanalApoio.objects.create(nome='Ligue 180', descricao='Central de atendimento', contato='180')

    def dados(self, **extra):
        return {
            'titulo': 'Conheça seus direitos',
            'categoria': 'direitos',
            'corpo': 'Primeiro parágrafo.\n\nSegundo parágrafo.',
            'canais_apoio': [self.canal.pk],
            **extra,
        }

    def test_formulario_nao_pede_autor(self):
        self.client.login(username='cae1', password=SENHA)
        resposta = self.client.get(reverse('novo_conteudo'))
        self.assertEqual(resposta.status_code, 200)
        self.assertNotIn('autor', resposta.context['form'].fields)

    def test_autor_e_o_membro_da_cae_logado(self):
        self.client.login(username='cae1', password=SENHA)
        resposta = self.client.post(reverse('novo_conteudo'), self.dados())
        self.assertRedirects(resposta, reverse('listar_conteudo'))
        conteudo = ConteudoEducativo.objects.get()
        self.assertEqual(conteudo.autor_id, self.cae.pk)
        self.assertEqual(list(conteudo.canais_apoio.all()), [self.canal])  # save_m2m funcionou

    def test_denunciante_nao_cria_conteudo(self):
        self.client.login(username='ana', password=SENHA)
        resposta = self.client.post(reverse('novo_conteudo'), self.dados())
        self.assertEqual(resposta.status_code, 403)
        self.assertEqual(ConteudoEducativo.objects.count(), 0)

    def test_detalhe_separa_paragrafos_e_mostra_autor_da_cae(self):
        conteudo = ConteudoEducativo.objects.create(
            titulo='T', categoria='direitos', corpo='Primeiro parágrafo.\n\nSegundo parágrafo.',
            autor=self.cae,
        )
        resposta = self.client.get(reverse('detalhar_conteudo', kwargs={'pk': conteudo.pk}))
        self.assertContains(resposta, '<p>Primeiro parágrafo.</p>')
        self.assertContains(resposta, '<p>Segundo parágrafo.</p>')
        self.assertContains(resposta, 'Marina Souza')

    def test_detalhe_escapa_html_do_corpo(self):
        conteudo = ConteudoEducativo.objects.create(
            titulo='T', categoria='direitos', corpo='<script>alert(1)</script>', autor=self.cae,
        )
        resposta = self.client.get(reverse('detalhar_conteudo', kwargs={'pk': conteudo.pk}))
        self.assertNotContains(resposta, '<script>alert(1)</script>')

    def test_detalhe_sem_autor_nao_quebra(self):
        conteudo = ConteudoEducativo.objects.create(titulo='T', categoria='direitos', corpo='x')
        resposta = self.client.get(reverse('detalhar_conteudo', kwargs={'pk': conteudo.pk}))
        self.assertEqual(resposta.status_code, 200)