import os
import boto3
import requests
from django.db import models
from django.conf import settings
from genres.models import Genre, Info
from utils.common import generate_hash
from django.core.files.storage import default_storage
from utils.common import delete_file_from_s3, delete_directory_from_s3


endpoint_storage_movies = settings.BASE_MOVIES_ENDPOINT
groups = (
    (1, 'LIVRE'),
    (2, '+10'),
    (3, '+12'),
    (4, '+16'),
    (5, '+18'),
)


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
    return f'movies/{instance.hashed_id}/{new_filename}'

def player_upload_path(instance, filename):
    # instance.id ainda não foi definido, usando UUID temporário
    instance.player_name = f'{filename}'
    return f'movies/{instance.hashed_id}/{filename}'


class Movie(models.Model):
    id = models.AutoField(primary_key=True)
    hashed_id = models.CharField(max_length=15, blank=True, null=True, unique=True)
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
    player = models.FileField(upload_to=player_upload_path, null=True, blank=True)
    player_name = models.CharField(max_length=100, default='', blank=True)
    file_size = models.PositiveIntegerField(null=True, blank=True, editable=False, default=0)
    
      
    def delete(self, *args, **kwargs):
        # Obtém o caminho do diretório a ser excluído
        directory_path = f'movies/{self.hashed_id}'
        print(f'Diretório a ser excluido{directory_path}')
        try:
            delete_directory_from_s3(directory_path);
        except Exception as e:
            print(f"Erro ao excluir o diretório do Amazon S3: {e}")
        super().delete(*args, **kwargs)

    def save(self, *args, **kwargs):
            if not self.hashed_id:
                self.hashed_id = generate_hash()

            if not self.id:
                last_movie = Movie.objects.order_by('-id').first()
                last_id = last_movie.id if last_movie else 0
                self.id = last_id + 1

            if self.player:
                self.file_size = self.player.size

                if self.player.name != self.player_name:
                    file = f'movies/{self.hashed_id}/{self.player_name}'
                    if self.player_name:
                        if delete_file_from_s3(file):
                            print("Arquivo deletado com sucesso!")
                        else:
                            print("Falha ao deletar o arquivo.")

                    self.player_name = self.player.name

                    # Novo código para monitorar o progresso de upload
                    s3 = boto3.client(
                        's3',
                        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                        region_name=settings.AWS_S3_REGION_NAME
                    )
                    bucket_name = settings.AWS_STORAGE_BUCKET_NAME
                    key = file

                    # Inicie o upload
                    s3.upload_fileobj(
                        self.player.file,
                        bucket_name,
                        key,
                        Callback=ProgressPercentage(self.player.size)
                    )

            super().save(*args, **kwargs)


# Função de callback para rastrear o progresso
class ProgressPercentage(object):
    def __init__(self, filename):
        self._filename = filename
        self._size = float(os.path.getsize(filename))
        self._seen_so_far = 0
        self._lock = threading.Lock()

    def __call__(self, bytes_amount):
        # Adicione o número de bytes transferidos ao total visto até agora
        with self._lock:
            self._seen_so_far += bytes_amount
            percentage = (self._seen_so_far / self._size) * 100
            print(f"Progresso de upload: {percentage:.2f}%")

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
