# validators.py
import re  # Adicione esta linha para importar o módulo re
from django.core.exceptions import ValidationError
from .backends.backends import EmailBackend
from django.contrib.auth.models import User
from utils.common import validate_date



def validate_login_credentials(request, email, password):
    user = EmailBackend().authenticate(request, email=email, password=password)
    if not user:
        raise ValidationError("Credenciais inválidas. Por favor, verifique o email e a senha.")
    response = validate_date(user)
    if response:
        raise ValidationError("Erro de acesso, conta atrasada, entre em contato com seu provedor")
    if not user.is_active:
        raise ValidationError("Usuário inativo. Entre em contato com o suporte.")
    


def validate_lowercase_username(value):
    if not re.match(r'^[a-zA-Z0-9@/./+/-/_/~ ]*$', value):
        raise ValidationError(
            "Informe um nome de usuário válido. Este valor pode conter letras maiúsculas, minúsculas, números, espaços e os seguintes caracteres especiais: @/./+/-/_."
        )


def validate_unique_email(email):
    if User.objects.filter(email=email).exists():
        raise ValidationError(str('Este endereço de e-mail já está em uso.'))


def validate_password_confirmation(password, password_confirmation):
    if password and password_confirmation and password != password_confirmation:
        raise ValidationError('A senha de confirmação não coincide com a senha.')