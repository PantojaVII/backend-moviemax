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
import shutil
import os
 

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



""" BOTO CONFIG R2 """
class R2FileManager:
    def __init__(self):
        self.s3_client = self.get_r2_client()
        self.r2_bucket_name = "coliseu-bitware-media"
    
    def get_r2_client(self):
        s3 = boto3.client(
            service_name="",
            endpoint_url='',
            aws_access_key_id='',
            aws_secret_access_key='',
            region_name="auto",
        )
        return s3
    
    def upload_file(self, file, path_to_file):
        try:
            self.s3_client.upload_fileobj(file, self.r2_bucket_name, path_to_file)
            print("Arquivo enviado com sucesso para o R2 da Cloudflare.")
            return f"/{path_to_file}"
        except Exception as e:
            print(f"Erro ao enviar arquivo para o R2 da Cloudflare via S3: {e}")
    
    def delete_file(self, path_to_file):
        try:
            self.s3_client.delete_object(Bucket=self.r2_bucket_name, Key=path_to_file)
            print("Arquivo deletado com sucesso do R2 da Cloudflare.")
        except Exception as e:
            print(f"Erro ao deletar arquivo do R2 da Cloudflare via S3: {e}")
    
    def delete_directory(self, directory_path):
        try:
            objects_to_delete = []
            paginator = self.s3_client.get_paginator('list_objects_v2')
            pages = paginator.paginate(Bucket=self.r2_bucket_name, Prefix=directory_path)
            for page in pages:
                if 'Contents' in page:
                    for obj in page['Contents']:
                        objects_to_delete.append({'Key': obj['Key']})
            
            if objects_to_delete:
                response = self.s3_client.delete_objects(Bucket=self.r2_bucket_name, Delete={'Objects': objects_to_delete})
                if 'Errors' in response:
                    for error in response['Errors']:
                        print(f"Erro ao excluir objeto {error['Key']}: {error['Code']}")
                else:
                    print("Diretório excluído com sucesso do R2 da Cloudflare.")
            else:
                print("Nenhum objeto encontrado no diretório para excluir.")
        except Exception as e:
            print(f"Erro ao excluir diretório do R2 da Cloudflare via S3: {e}")





def delete_file_local(path_to_file):
    try:
        full_directory_path = os.path.join(settings.MEDIA_ROOT, path_to_file)
        os.remove(full_directory_path)
        print("Arquivo excluído com sucesso localmente.")
    except Exception as e:
        print(f"Erro ao excluir arquivo localmente: {e}")

def delete_directory_local(directory_path):
    try:
        # Construa o caminho completo do diretório usando MEDIA_URL
        full_directory_path = os.path.join(settings.MEDIA_ROOT, directory_path)
        
        # Verifique se o diretório existe antes de tentar excluí-lo
        if os.path.exists(full_directory_path):
            # Exclui o diretório e todos os seus conteúdos
            shutil.rmtree(full_directory_path)
            print("Diretório e todos os seus conteúdos excluídos com sucesso localmente.")
        else:
            print("O diretório não existe.")
    except Exception as e:
        print(f"Erro ao excluir diretório localmente: {e}")



""" def delete_file_from_s3(file):
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
        print(f"Erro ao excluir o diretório do Amazon S3: {e}") """