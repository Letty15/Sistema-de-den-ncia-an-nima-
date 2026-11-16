import io
import shutil
import tempfile

from django.contrib.auth.models import Group, User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.urls import reverse
from PIL import Image as PILImage

from usuarios.models import Usuario
from .models import Denuncia, TipoViolencia

MEDIA_TESTE = tempfile.mkdtemp()
SENHA = 'senha-forte-123'


def imagem_teste(nome='foto.png', formato='PNG', tamanho=(20, 10)):
    buffer = io.BytesIO()
    PILImage.new('RGB', tamanho, 'purple').save(buffer, formato)
    tipo = 'image/png' if formato == 'PNG' else 'image/jpeg'
    return SimpleUploadedFile(nome, buffer.getvalue(), content_type=tipo)


@override_settings(MEDIA_ROOT=MEDIA_TESTE)
class BaseDenunciaTest(TestCase):
    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(MEDIA_TESTE, ignore_errors=True)

    def setUp(self):
        self.tipo = TipoViolencia.objects.create(nome='Assédio')

        self.ana = Usuario(username='ana', cpf='111.111.111-11', rg='1111', endereco='Rua A')
        self.ana.set_password(SENHA)
        self.ana.save()
        self.ana.groups.add(Group.objects.get(name='Denunciante'))

        self.cae = User.objects.create_user('cae1', password=SENHA)
        self.cae.groups.add(Group.objects.get(name='CAE'))

        self.denuncia = Denuncia.objects.create(
            tipo_violencia=self.tipo, denunciante=self.ana, descricao='Relato de teste',
        )

    def dados_nova_denuncia(self, **extra):
        return {'tipo_violencia': self.tipo.pk, 'descricao': 'Nova situação', **extra}


class EvidenciaTest(BaseDenunciaTest):
    def setUp(self):
        super().setUp()
        self.client.login(username='ana', password=SENHA)
        self.url = reverse('nova_denuncia')

    def test_denuncia_sem_evidencia(self):
        resposta = self.client.post(self.url, self.dados_nova_denuncia())
        self.assertEqual(resposta.status_code, 302)
        self.assertEqual(Denuncia.objects.count(), 2)

    def test_denuncia_com_evidencias_guarda_dados_da_imagem(self):
        resposta = self.client.post(self.url, self.dados_nova_denuncia(
            evidencias=[imagem_teste('a.png'), imagem_teste('b.png', tamanho=(40, 30))],
        ))
        self.assertEqual(resposta.status_code, 302)
        denuncia = Denuncia.objects.exclude(pk=self.denuncia.pk).get()
        self.assertEqual(denuncia.evidencias.count(), 2)
        primeira = denuncia.evidencias.order_by('pk').first()
        self.assertEqual((primeira.largura, primeira.altura, primeira.formato), (20, 10, 'PNG'))

    def test_arquivo_que_nao_e_imagem_e_recusado(self):
        falso = SimpleUploadedFile('falso.png', b'isto nao e uma imagem', content_type='image/png')
        resposta = self.client.post(self.url, self.dados_nova_denuncia(evidencias=[falso]))
        self.assertEqual(resposta.status_code, 200)
        self.assertContains(resposta, 'não é uma imagem válida')
        self.assertEqual(Denuncia.objects.count(), 1)  # nada foi salvo

    def test_limite_de_imagens(self):
        arquivos = [imagem_teste(f'{i}.png') for i in range(6)]
        resposta = self.client.post(self.url, self.dados_nova_denuncia(evidencias=arquivos))
        self.assertEqual(resposta.status_code, 200)
        self.assertContains(resposta, 'no máximo 5 imagens')
        self.assertEqual(Denuncia.objects.count(), 1)

    def test_remover_evidencia_ao_editar(self):
        self.client.post(self.url, self.dados_nova_denuncia(evidencias=[imagem_teste()]))
        denuncia = Denuncia.objects.exclude(pk=self.denuncia.pk).get()
        evidencia = denuncia.evidencias.get()

        resposta = self.client.post(
            reverse('editar_denuncia', kwargs={'protocolo': denuncia.protocolo}),
            {'tipo_violencia': self.tipo.pk, 'descricao': 'Editada',
             'remover_evidencias': [evidencia.pk]},
        )
        self.assertEqual(resposta.status_code, 302)
        self.assertEqual(denuncia.evidencias.count(), 0)


class StatusTest(BaseDenunciaTest):
    def setUp(self):
        super().setUp()
        self.url_status = reverse('alterar_status_denuncia', kwargs={'protocolo': self.denuncia.protocolo})
        self.url_detalhe = reverse('detalhar_denuncia', kwargs={'protocolo': self.denuncia.protocolo})

    def test_cae_altera_status(self):
        self.client.login(username='cae1', password=SENHA)
        resposta = self.client.post(self.url_status, {'status': 'em_analise'})
        self.assertRedirects(resposta, self.url_detalhe)
        self.denuncia.refresh_from_db()
        self.assertEqual(self.denuncia.status, 'em_analise')

    def test_denunciante_nao_altera_status(self):
        self.client.login(username='ana', password=SENHA)
        self.assertEqual(self.client.get(self.url_status).status_code, 403)
        self.assertEqual(self.client.post(self.url_status, {'status': 'concluida'}).status_code, 403)
        self.denuncia.refresh_from_db()
        self.assertEqual(self.denuncia.status, 'pendente')

    def test_botao_de_status_so_aparece_para_cae(self):
        self.client.login(username='ana', password=SENHA)
        self.assertNotContains(self.client.get(self.url_detalhe), 'Alterar status')
        self.client.logout()
        self.client.login(username='cae1', password=SENHA)
        self.assertContains(self.client.get(self.url_detalhe), 'Alterar status')

    def test_lista_filtra_por_status(self):
        Denuncia.objects.create(
            tipo_violencia=self.tipo, denunciante=self.ana, descricao='Outra', status='concluida',
        )
        self.client.login(username='cae1', password=SENHA)
        resposta = self.client.get(reverse('listar_denuncia'), {'status': 'concluida'})
        self.assertEqual(len(resposta.context['denuncias']), 1)
        self.assertEqual(resposta.context['denuncias'][0].status, 'concluida')