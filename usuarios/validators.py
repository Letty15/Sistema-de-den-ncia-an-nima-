
from django.core.exceptions import ValidationError
import re


def validar_cpf(cpf):
    cpf = re.sub(r'\D', '', cpf or '')

    if len(cpf) != 11:
        raise ValidationError('O CPF deve conter 11 dígitos.')

    if cpf == cpf[0] * 11:
        raise ValidationError('Informe um CPF válido.')

    # Primeiro dígito verificador
    soma = sum(
        int(cpf[i]) * (10 - i)
        for i in range(9)
    )

    resto = (soma * 10) % 11
    primeiro_digito = 0 if resto == 10 else resto

    if primeiro_digito != int(cpf[9]):
        raise ValidationError('CPF inválido.')

    # Segundo dígito verificador
    soma = sum(
        int(cpf[i]) * (11 - i)
        for i in range(10)
    )

    resto = (soma * 10) % 11
    segundo_digito = 0 if resto == 10 else resto

    if segundo_digito != int(cpf[10]):
        raise ValidationError('CPF inválido.')
