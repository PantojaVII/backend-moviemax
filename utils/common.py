# utils/common.py
import hashlib
import boto3
from django.conf import settings
from datetime import datetime
from accounts.models import Profile
from django.utils import timezone
from django.http import JsonResponse
from botocore.exceptions import ClientError
import uuid
 
 

def generate_hash():
    # Gera um UUID aleatório
    random_uuid = uuid.uuid4()

    # Obtém a data e hora atual
    current_datetime = datetime.now()

    # Converte a data e hora em uma string formatada
    datetime_str = current_datetime.strftime("%Y-%m-%d %H:%M:%S")

    # Concatena o UUID e a string formatada da data e hora
    combined_str = f"{random_uuid}-{datetime_str}"

    # Gera um hash usando SHA-256
    hashed_value = hashlib.sha256(combined_str.encode()).hexdigest()

    return hashed_value[:15]  # Retorna apenas os primeiros 15 caracteres do hash



def validate_date(user):

    profile = Profile.objects.get(user=user)
    # Obtenha a data e hora local atual

    current_datetime_local = timezone.localtime(timezone.now())
    if current_datetime_local.date() > profile.date_block:
        print(profile.date_block)
        return JsonResponse({"error": "Erro de acesso, conta atrasada, entre em contato com seu provedor"}, status=400)

def delete_file_from_s3(file):
    s3 = boto3.client('s3', aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)
    s3_bucket = settings.AWS_S3_CUSTOM_DOMAIN

    try:
        # Delete the file
        s3.delete_object(Bucket=s3_bucket, Key=file)
        return True
    except ClientError as e:
        # Log the error
        print(f"An error occurred while deleting the file: {e}")
        return False

def delete_directory_from_s3(path):
    try:
        # Remove o diretório correspondente no Amazon S3
        s3 = boto3.client('s3', aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)
        s3_bucket = settings.AWS_S3_CUSTOM_DOMAIN
        s3_directory = path
        s3_objects = s3.list_objects_v2(Bucket=s3_bucket, Prefix=s3_directory)
        if 'Contents' in s3_objects:
            for obj in s3_objects['Contents']:
                s3.delete_object(Bucket=s3_bucket, Key=obj['Key'])
            print(f"Diretório {s3_directory} excluído com sucesso do Amazon S3.")
        else:
            print(f"Diretório {s3_directory} não existe no Amazon S3.")
    except Exception as e:
        print(f"Erro ao excluir o diretório do Amazon S3: {e}")