import os
from django.db import models
import requests
from genres.models import Genre, Info
from companies.models import Companie
from django.conf import settings
from utils.common import generate_hash
import boto3
endpoint_storage_episodes = settings.BASE_EPISODES_ENDPOINT
endpoint_destroy_season = settings.BASE_SEASON_DESTROY_ENDPOINT
endpoint_destroy_series = settings.BASE_SERIES_DESTROY_ENDPOINT

groups = (
    (1, 'LIVRE'),
    (2, '+10'),
    (3, '+12'),
    (4, '+16'),
    (5, '+18'),
);


def movie_upload_path(instance, filename):
    # Obtém a extensão do arquivo original
    extension = filename.split('.')[-1]

    # Define um novo nome de arquivo baseado no campo ao qual o arquivo pertence
    if instance.coverOne.name == filename:
        new_filename = 'coverOne.' + extension
    elif instance.coverTwo.name == filename:
        new_filename = 'coverTwo.' + extension
    elif instance.highlight.name == filename:
        new_filename = 'highlight.' + extension
    else:
        # Se o arquivo não corresponder a nenhum dos campos esperados, mantém o nome original
        new_filename = filename

    # Retorna o caminho completo do arquivo com o novo nome
    return f'series/{instance.hashed_id}/{new_filename}'
def episode_upload_path(instance, filename):
    return f'series/{instance.season.serie.id}/Season {instance.season.season}/{filename}'

class Serie(models.Model):
    id = models.AutoField(primary_key=True)
    hashed_id = models.CharField(max_length=64, blank=True, null=True, unique=True)
    name = models.CharField(max_length=100)
    synopsis = models.TextField()
    release_date = models.DateField()
    director = models.CharField(max_length=100)
    genres = models.ManyToManyField(Genre, related_name='series')
    info = models.ManyToManyField(Info)
    rating = models.CharField(max_length=3, default=0)
    playerTrailer = models.URLField(default=False)
    age_groups = models.IntegerField(choices=groups, default=1)
    company = models.ForeignKey(Companie, on_delete=models.CASCADE)
    coverOne = models.FileField(upload_to=movie_upload_path, default=0)
    coverTwo = models.FileField(upload_to=movie_upload_path, default=0)
    highlight = models.FileField(upload_to=movie_upload_path, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def delete(self, *args, **kwargs):
        # Obtém o caminho do diretório a ser excluído
        directory_path = f'series/{self.hashed_id}'
        print(f'Diretório a ser excluido{directory_path}')
        try:
            # Verifica se o diretório existe antes de tentar removê-lo
            if os.path.exists(directory_path):
                # Remove todos os arquivos dentro do diretório
                for filename in os.listdir(directory_path):
                    file_path = os.path.join(directory_path, filename)
                    os.remove(file_path)
                # Remove o diretório vazio
                os.rmdir(directory_path)
                print(f"Diretório {directory_path} excluído com sucesso.")
            else:
                print(f"Diretório {directory_path} não existe.")
        except Exception as e:
            print(f"Erro ao excluir o diretório local: {e}")
        # Chama o método delete da classe pai para excluir o objeto Movie do banco de dados
        try:
            # Remove o diretório correspondente no Amazon S3
            s3 = boto3.client('s3', aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                              aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)
            s3_bucket = settings.AWS_STORAGE_BUCKET_NAME
            s3_directory = f"series/{self.hashed_id}/"
            s3_objects = s3.list_objects_v2(Bucket=s3_bucket, Prefix=s3_directory)
            if 'Contents' in s3_objects:
                for obj in s3_objects['Contents']:
                    s3.delete_object(Bucket=s3_bucket, Key=obj['Key'])
                print(f"Diretório {s3_directory} excluído com sucesso do Amazon S3.")
            else:
                print(f"Diretório {s3_directory} não existe no Amazon S3.")
        except Exception as e:
            print(f"Erro ao excluir o diretório do Amazon S3: {e}")
        super().delete(*args, **kwargs)



    def save(self, *args, **kwargs):
        if not self.hashed_id:
            self.hashed_id = generate_hash()
        # Se o objeto ainda não tem um ID, isso significa que é um novo objeto
        if not self.id:
            last_serie = Serie.objects.order_by('-id').first()
            last_id = last_serie.id if last_serie else 0
            self.id = last_id + 1

        # Chame o método save() da classe pai para realizar o salvamento real
        super().save(*args, **kwargs)
    def __str__(self):
        return f'{self.name} - {self.release_date}'
class Season(models.Model):
    serie = models.ForeignKey(Serie, on_delete=models.CASCADE)   
    hashed_id = models.CharField(max_length=64, blank=True, null=True, unique=True)
    season = models.PositiveSmallIntegerField()  # temporada   
    synopsis = models.TextField()
    release_date = models.DateField()  # Data de lançamento da temporada
    created_at = models.DateTimeField(auto_now_add=True)  # Data e hora de criação do registro
    updated_at = models.DateTimeField(auto_now=True)  # Data e hora da última atualização

    def __str__(self):
        return f"{self.serie} - Temporada {self.season}"

    def save(self, *args, **kwargs):
        if not self.hashed_id:
            self.hashed_id = generate_hash()
        super().save(*args, **kwargs)
    def delete(self, *args, **kwargs):
        # Obtém o caminho do diretório a ser excluído
        directory_path = f'{self.serie.hashed_id}/season_{self.season}/'
        print(f'Diretório a ser excluido{directory_path}')
        try:
            # Verifica se o diretório existe antes de tentar removê-lo
            if os.path.exists(directory_path):
                # Remove todos os arquivos dentro do diretório
                for filename in os.listdir(directory_path):
                    file_path = os.path.join(directory_path, filename)
                    os.remove(file_path)
                # Remove o diretório vazio
                os.rmdir(directory_path)
                print(f"Diretório {directory_path} excluído com sucesso.")
            else:
                print(f"Diretório {directory_path} não existe.")
        except Exception as e:
            print(f"Erro ao excluir o diretório local: {e}")
        # Chama o método delete da classe pai para excluir o objeto Movie do banco de dados
        try:
            # Remove o diretório correspondente no Amazon S3
            s3 = boto3.client('s3', aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                              aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)
            s3_bucket = settings.AWS_STORAGE_BUCKET_NAME
            s3_directory = f"movies/{self.id}/"
            s3_objects = s3.list_objects_v2(Bucket=s3_bucket, Prefix=s3_directory)
            if 'Contents' in s3_objects:
                for obj in s3_objects['Contents']:
                    s3.delete_object(Bucket=s3_bucket, Key=obj['Key'])
                print(f"Diretório {s3_directory} excluído com sucesso do Amazon S3.")
            else:
                print(f"Diretório {s3_directory} não existe no Amazon S3.")
        except Exception as e:
            print(f"Erro ao excluir o diretório do Amazon S3: {e}")
        super().delete(*args, **kwargs)
class Episode(models.Model):
    season = models.ForeignKey(Season, on_delete=models.CASCADE, related_name='episodes')
    hashed_id = models.CharField(max_length=64, blank=True, null=True, unique=True)  
    num_episode  = models.PositiveSmallIntegerField()  # numero episode   
    name = models.CharField(max_length=100)  # Nome do episódio
    duration = models.DurationField()  # Duração do episódio
    synopsis = models.TextField()
    player = models.FileField(null=True, blank=True)
    playerURL = models.URLField(default='', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)  # Data e hora de criação do registro
    updated_at = models.DateTimeField(auto_now=True)  # Data e hora da última atualização
    file_size = models.PositiveIntegerField(null=True, blank=True, editable=False,default=0)
    def __str__(self):
        return f"{self.season} - Episódio {self.name}"

    def send_player_to_endpoint(self, endpoint):
        try:

            # Prepara os dados para a solicitação POST
            data = {'queops_id_episode': self.hashed_id,
                    'path': f'{self.season.serie.hashed_id}/season_{self.season.season}/'}
            files = {'episode': self.player}

            response = requests.post(endpoint, data=data, files=files)
            if response.status_code == 200:
                return response.json().get('path')

        except Exception as e:
            print(f"Erro ao enviar o player para o endpoint: {e}")


    def save(self, *args, **kwargs):
        # Se hashed_id não estiver definido, gera um hash e atribui
        if not self.hashed_id:
            self.hashed_id = generate_hash()


        # Se houver um arquivo de player associado
        try:
            if self.player:
                # Calcula o tamanho do arquivo em bytes
                self.file_size = self.player.size
                old_episode = Episode.objects.get(id=self.id)
                # Verifica se o arquivo do player é diferente do que está armazenado no banco de dados
                if self.id and self.player.name != old_episode.player:
                    # Envia o arquivo do player para o endpoint e atualiza o campo playerURL
                    self.playerURL = self.send_player_to_endpoint(f"{endpoint_storage_episodes}"
                                                                  f"{self.hashed_id}")
                    self.player = self.player.name
        except Episode.DoesNotExist:
            self.playerURL = self.send_player_to_endpoint(f"{endpoint_storage_episodes}");
            self.player = self.player.name

        # Chama o método save da classe pai
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # Obtém o caminho do diretório a ser excluído
        directory_path = f'{self.serie.hashed_id}/season_{self.season.season}/{self.player}'
        print(f'Diretório a ser excluido{directory_path}')
        try:
            # Verifica se o diretório existe antes de tentar removê-lo
            if os.file.exists(directory_path):
                # Remove o episode
                os.remove(file_path)
                print(f"episode {self.player} excluído com sucesso.")
            else:
                print(f"episode {self.player} não existe.")
        except Exception as e:
            print(f"Erro ao excluir o episode local: {e}")
        # Chama o método delete da classe pai para excluir o objeto Movie do banco de dados
        try:
            # Remove o diretório correspondente no Amazon S3
            s3 = boto3.client('s3', aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                              aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)
            s3_bucket = settings.AWS_STORAGE_BUCKET_NAME
            s3_key = f'{self.serie.hashed_id}/season_{self.season.season}/{self.player}'

            # Verifica se o objeto existe antes de tentar removê-lo
            response = s3.list_objects_v2(Bucket=s3_bucket, Prefix=s3_key)
            if 'Contents' in response:
                # Remove o objeto (arquivo) do S3
                s3.delete_object(Bucket=s3_bucket, Key=s3_key)
                print(f"Arquivo {s3_key} excluído com sucesso do Amazon S3.")
            else:
                print(f"Arquivo {s3_key} não existe no Amazon S3.")

        except Exception as e:
            print(f"Erro ao excluir o arquivo do Amazon S3: {e}")

        # Chama o método delete da classe pai para excluir o objeto do banco de dados
        super().delete(*args, **kwargs)

