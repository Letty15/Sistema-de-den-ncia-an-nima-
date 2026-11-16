from django.contrib.auth.models import Group, User
from django.test import TestCase
from django.urls import reverse

from denuncias.models import Denuncia, TipoViolencia
from .models import Usuario

SENHA = 'senha-forte-123'


def criar_usuario(username, cpf, grupo='Denunciante'):
    usuario = Usuario(username=username, cpf=cpf, rg=cpf[:4], endereco='Rua A')
    usuario.set_password(SENHA)
    usuario.save()
    usuario.groups.add(Group.objects.get(name=grupo))
    return usuario


class UsuarioTest(TestCase):
    def setUp(self):
        self.cae = User.objects.create_user('cae1', password=SENHA)
        self.cae.groups.add(Group.objects.get(name='CAE'))
        self.ana = criar_usuario('ana', '111.111.111-11')

    def test_cae_lista_usuarios(self):
        self.client.login(username='cae1', password=SENHA)
        resposta = self.client.get(reverse('listar_usuario'))
        self.assertContains(resposta, 'ana')

    def test_denunciante_nao_lista_usuarios(self):
        self.client.login(username='ana', password=SENHA)
        self.assertEqual(self.client.get(reverse('listar_usuario')).status_code, 403)

    def test_editar_usuario_mostra_mensagem_de_sucesso(self):
        self.client.login(username='cae1', password=SENHA)
        resposta = self.client.post(
            reverse('editar_usuario', kwargs={'pk': self.ana.pk}),
            {'username': 'ana', 'email': 'ana@exemplo.com', 'cpf': '111.111.111-11',
             'rg': '1111', 'endereco': 'Rua B'},
            follow=True,
        )
        self.assertContains(resposta, 'Dados do usuário atualizados')
        self.ana.refresh_from_db()
        self.assertEqual(self.ana.endereco, 'Rua B')

    def test_cae_exclui_usuario_sem_denuncias(self):
        self.client.login(username='cae1', password=SENHA)
        resposta = self.client.post(reverse('deletar_usuario', kwargs={'pk': self.ana.pk}))
        self.assertRedirects(resposta, reverse('listar_usuario'))
        self.assertFalse(Usuario.objects.filter(pk=self.ana.pk).exists())

    def test_usuario_com_denuncias_nao_e_excluido(self):
        Denuncia.objects.create(
            tipo_violencia=TipoViolencia.objects.create(nome='Assédio'),
            denunciante=self.ana, descricao='Relato',
        )
        self.client.login(username='cae1', password=SENHA)
        resposta = self.client.post(reverse('deletar_usuario', kwargs={'pk': self.ana.pk}), follow=True)
        self.assertContains(resposta, 'denúncias registradas')
        self.assertTrue(Usuario.objects.filter(pk=self.ana.pk).exists())

    def test_nao_exclui_a_propria_conta(self):
        maria = criar_usuario('maria', '222.222.222-22', grupo='CAE')  # Usuario com permissão de excluir
        self.client.login(username='maria', password=SENHA)
        resposta = self.client.post(reverse('deletar_usuario', kwargs={'pk': maria.pk}), follow=True)
        self.assertContains(resposta, 'própria conta')
        self.assertTrue(Usuario.objects.filter(pk=maria.pk).exists())