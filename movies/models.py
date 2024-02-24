import os
import boto3
import requests
from django.db import models
from django.conf import settings
from genres.models import Genre, Info
from utils.common import generate_hash
from django.core.files.storage import default_storage
from utils.common import *
from django.shortcuts import get_object_or_404


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
    player = models.FileField(null=True, blank=True)
    player_name = models.CharField(max_length=100, default='', blank=True)
    file_size = models.PositiveIntegerField(null=True, blank=True, editable=False, default=0)
    
      
    def delete(self, *args, **kwargs):
        # Obtém o caminho do diretório a ser excluído
        directory_path = f'movies/{self.hashed_id}'
        print(f'Diretório a ser excluido {directory_path}')
        try:
            file_manager = R2FileManager()
            file_manager.delete_directory(directory_path);
            delete_directory_local(directory_path)
        except Exception as e:
            print(f"Erro ao excluir o diretório do Amazon S3: {e}")
        super().delete(*args, **kwargs)

    def save(self, *args, **kwargs):
            
            movie = Movie.objects.filter(id=self.id).first()
            
            if movie is None:
                self.hashed_id = generate_hash()
                if self.player:
                    self.player_name = self.player.name
                    self.file_size = self.player.size
                    file_manager = R2FileManager()
                    self.player = file_manager.upload_file(
                        file=self.player.file, 
                        path_to_file=f"movies/{self.hashed_id}/{self.player.name}"
                        )
            else:
                if self.player:
                    file_manager = R2FileManager()
                    file_manager.delete_file(path_to_file=f"movies/{movie.hashed_id}/{movie.player_name}")
                    self.player_name = self.player.name
                    self.file_size = self.player.size
                    self.player = file_manager.upload_file(
                        file=self.player.file, 
                        path_to_file=f"movies/{self.hashed_id}/{self.player.name}"
                        )
                    
            super().save(*args, **kwargs)

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
