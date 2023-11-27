# validators.py
from django.core.exceptions import ValidationError
from .backends.backends import EmailBackend
from django.contrib.auth.models import User


def validate_login_credentials(request, email, password):
    user = EmailBackend().authenticate(request, email=email, password=password)
    if not user:
        raise ValidationError("Credenciais inválidas. Por favor, verifique o email e a senha.")


def validate_lowercase_username(value):
    if not value.islower():
        raise ValidationError("O nome de usuário deve estar em minúsculas.")


def validate_unique_email(email):
    if User.objects.filter(email=email).exists():
        raise ValidationError(str('Este endereço de e-mail já está em uso.'))


def validate_password_confirmation(password, password_confirmation):
    if password and password_confirmation and password != password_confirmation:
        raise ValidationError('A senha de confirmação não coincide com a senha.')