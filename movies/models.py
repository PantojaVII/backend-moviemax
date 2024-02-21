import os
import boto3
import requests
from django.db import models
from django.conf import settings
from genres.models import Genre, Info
from utils.common import generate_hash

endpoint_storage_movies = settings.BASE_MOVIES_ENDPOINT
groups = (
    (1, 'LIVRE'),
    (2, '+10'),
    (3, '+12'),
    (4, '+16'),
    (5, '+18'),
)


def movie_upload_path(instance, filename):
    # instance.id ainda não foi definido, usando UUID temporário
    instance.playerURL = f'{settings.MEDIA_URL}/movies/{instance.hashed_id}/{filename}'
    return f'movies/{instance.hashed_id}/{filename}'


class Movie(models.Model):
    id = models.AutoField(primary_key=True)
    hashed_id = models.CharField(max_length=64, blank=True, null=True, unique=True)
    name = models.CharField(max_length=100)
    synopsis = models.TextField()
    duration = models.DurationField()
    playerTrailer = models.URLField(default=False)
    company = models.ForeignKey('companies.Companie', on_delete=models.CASCADE)
    release_date = models.DateField()
    director = models.CharField(max_length=100)
    genres = models.ManyToManyField(Genre)
    info = models.ManyToManyField(Info)
    rating = models.CharField(max_length=3, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    age_groups = models.IntegerField(choices=groups, default=1)
    updated_at = models.DateTimeField(auto_now=True)
    coverOne = models.FileField(upload_to=movie_upload_path)
    coverTwo = models.FileField(upload_to=movie_upload_path)
    highlight = models.FileField(upload_to=movie_upload_path)
    player = models.FileField(upload_to=movie_upload_path, null=True, blank=True)
    playerURL = models.URLField(default='', blank=True)
    file_size = models.PositiveIntegerField(null=True, blank=True, editable=False, default=0)

    def send_player_to_endpoint_laravel(self, endpoint):
        try:

            # Prepara os dados para a solicitação POST
            data = {'queops_id_movie': self.hashed_id,
                    'path': f'{self.hashed_id}/'}
            files = {'movie': self.player}

            # Envia a solicitação POST com o arquivo player e os dados adicionais
            response = requests.post(endpoint, data=data, files=files)
            if response.status_code == 200:
                return response.json().get('path')

        except Exception as e:
            print(f"Erro ao enviar o player para o endpoint: {e}")
    def send_player_to_endpoint(self):
        try:
            # Verifica se existe um arquivo player associado ao objeto Movie
            if self.player:
                # Caminho onde o arquivo player será armazenado no Amazon S3
                player_path = f"movies/{self.id}/{self.player.name}"

                self.save()

                return player_url
            else:
                print("Nenhum arquivo player associado a este filme.")
        except Exception as e:
            print(f"Erro ao enviar o player para o Amazon S3: {e}")

    def save(self, *args, **kwargs):
        # Se hashed_id não estiver definido, gera um hash e atribui
        if not self.hashed_id:
            self.hashed_id = generate_hash()

        # Se o objeto ainda não foi salvo (nenhum id atribuído)
        if not self.id:
            # Obtém o último objeto de filme
            last_movie = Movie.objects.order_by('-id').first()
            last_id = last_movie.id if last_movie else 0
            # Atribui um novo id incrementado ao objeto
            self.id = last_id + 1

        if self.player:
            # Atualiza o tamanho do arquivo em bytes
            self.file_size = self.player.size

        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # Obtém o caminho do diretório a ser excluído
        directory_path = f'movies/{self.hashed_id}'
        print(f'Diretório a ser excluido{directory_path}')
        try:
            # Remove o diretório correspondente no Amazon S3
            s3 = boto3.client('s3', aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                              aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)
            s3_bucket = settings.AWS_STORAGE_BUCKET_NAME
            s3_directory = f"movies/{self.hashed_id}/"
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


