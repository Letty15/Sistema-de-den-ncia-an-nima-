"""Validação e gravação das imagens de evidência de uma denúncia."""
from django.core.exceptions import ValidationError
from PIL import Image

from .models import Imagem

TAMANHO_MAXIMO_MB = 5
MAX_EVIDENCIAS = 5
FORMATOS_PERMITIDOS = {'JPEG', 'PNG', 'WEBP'}


def _ler_imagem(arquivo):
    """Confere tamanho e conteúdo; devolve (largura, altura, formato)."""
    if arquivo.size > TAMANHO_MAXIMO_MB * 1024 * 1024:
        raise ValidationError(f'"{arquivo.name}" é maior que {TAMANHO_MAXIMO_MB} MB.')
    try:
        img = Image.open(arquivo)
        img.verify()          # detecta arquivo corrompido ou que não é imagem
        arquivo.seek(0)
        img = Image.open(arquivo)  # verify() invalida o objeto: abre de novo
        largura, altura = img.size
        formato = img.format
    except Exception:
        raise ValidationError(f'"{arquivo.name}" não é uma imagem válida.') from None
    arquivo.seek(0)
    if formato not in FORMATOS_PERMITIDOS:
        raise ValidationError(f'"{arquivo.name}" precisa ser JPG, PNG ou WEBP.')
    return largura, altura, formato


def validar_evidencias(arquivos, ja_existentes=0):
    """Valida todos os arquivos enviados.

    Devolve uma lista de (arquivo, largura, altura, formato) ou levanta
    ValidationError com todas as mensagens de erro.
    """
    if ja_existentes + len(arquivos) > MAX_EVIDENCIAS:
        raise ValidationError(f'Cada denúncia pode ter no máximo {MAX_EVIDENCIAS} imagens.')

    validadas, erros = [], []
    for arquivo in arquivos:
        try:
            validadas.append((arquivo, *_ler_imagem(arquivo)))
        except ValidationError as e:
            erros.extend(e.messages)
    if erros:
        raise ValidationError(erros)
    return validadas


def salvar_evidencias(denuncia, validadas):
    """Cria um registro Imagem para cada arquivo já validado."""
    for arquivo, largura, altura, formato in validadas:
        Imagem.objects.create(
            denuncia=denuncia,
            largura=largura,
            altura=altura,
            formato=formato,
            dados=arquivo,
        )


def apagar_arquivos(imagens):
    """Apaga do disco os arquivos de imagens que já foram removidas do banco."""
    for imagem in imagens:
        imagem.dados.delete(save=False)