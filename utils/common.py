# utils/common.py
import hashlib
from datetime import datetime
from accounts.models import Profile
from django.utils import timezone
from django.http import JsonResponse


def generate_hash():
    # Obtém a data e hora atual
    current_datetime = datetime.now()

    # Converte a data e hora em uma string formatada
    datetime_str = current_datetime.strftime("%Y-%m-%d %H:%M:%S")

    # Gera um hash usando SHA-256
    hashed_value = hashlib.sha256(datetime_str.encode()).hexdigest()

    return hashed_value


def validate_date(user):

    profile = Profile.objects.get(user=user)
    # Obtenha a data e hora local atual

    current_datetime_local = timezone.localtime(timezone.now())
    if current_datetime_local.date() > profile.date_block:
        print(profile.date_block)
        return JsonResponse({"error": "Erro de acesso, conta atrasada, entre em contato com seu provedor"}, status=400)
