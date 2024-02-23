import os
from django.db import models
import requests
from genres.models import Genre, Info
from companies.models import Companie
from django.conf import settings
from utils.common import generate_hash
import boto3
from utils.common import delete_file_from_s3, delete_directory_from_s3


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
        # instance.id ainda não foi definido, usando UUID temporário
    instance.player_name = f'{filename}'
    return f'series/{instance.season.serie.hashed_id}/{instance.season.hashed_id}/{instance.player_name}'

""" ------------------------------------------------------------------------------ """

class Serie(models.Model):
    id = models.AutoField(primary_key=True)
    hashed_id = models.CharField(max_length=15, blank=True, null=True, unique=True)
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

        """ Abaixo apagamos o diretório do S3 """
        print(f'Diretório a ser excluido{directory_path}')
        try:
            delete_directory_from_s3(directory_path);
        except Exception as e:
            print(f"Erro ao excluir o diretório do Amazon S3: {e}")
        super().delete(*args, **kwargs)

    
""" ------------------------------------------------------------------------------ """


class Season(models.Model):
    serie = models.ForeignKey(Serie, on_delete=models.CASCADE)   
    hashed_id = models.CharField(max_length=15, blank=True, null=True, unique=True)
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
        directory_path = f'series/{self.serie.hashed_id}/{self.hashed_id}'
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
        """ Abaixo apagamos o diretório do S3 """
        print(f'Diretório a ser excluido{directory_path}')
        try:
            delete_directory_from_s3(directory_path);
        except Exception as e:
            print(f"Erro ao excluir o diretório do Amazon S3: {e}")
        super().delete(*args, **kwargs)

""" ------------------------------------------------------------------------------ """

class Episode(models.Model):

    season = models.ForeignKey(Season, on_delete=models.CASCADE, related_name='episodes')
    hashed_id = models.CharField(max_length=15, blank=True, null=True, unique=True)  
    num_episode  = models.PositiveSmallIntegerField()  # numero episode   
    name = models.CharField(max_length=100)  # Nome do episódio
    duration = models.DurationField()  # Duração do episódio
    synopsis = models.TextField()
    player = models.FileField(upload_to=episode_upload_path, null=True, blank=True)
    player_name = models.CharField(max_length=100, default='', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)  # Data e hora de criação do registro
    updated_at = models.DateTimeField(auto_now=True)  # Data e hora da última atualização
    file_size = models.PositiveIntegerField(null=True, blank=True, editable=False,default=0)
    def __str__(self):
        return f"{self.season} - Episódio {self.name}"

    def save(self, *args, **kwargs):
        # Se hashed_id não estiver definido, gera um hash e atribui
        if not self.hashed_id:
            self.hashed_id = generate_hash()

        # Se houver um arquivo de player associado
        if self.player:
            # Atualiza o tamanho do arquivo em bytes
            self.file_size = self.player.size

            # Verifica se o novo player é diferente do player_name atual
            if self.player.name != self.player_name:
                file = f'series/{self.season.serie.hashed_id}/{self.season.hashed_id}/{self.player_name}'
                # Deleta o player antigo se existir
                if self.player_name:
                    if delete_file_from_s3(file):
                        print("Arquivo deletado com sucesso!")
                    else:
                        print("Falha ao deletar o arquivo.")
                    

                # Atualiza o player_name com o nome do novo player
                self.player_name = self.player.name

        super().save(*args, **kwargs)


    def delete(self, *args, **kwargs):
        # Obtém o caminho do diretório a ser excluído
        file_path = f'series/{self.season.serie.hashed_id}/{self.season.hashed_id}/{self.player_name}'
        print(f'Arquivo a ser excluido{file_path}')
        try:
            delete_file_from_s3(file_path);
        except Exception as e:
            print(f"Erro ao excluir o diretório do Amazon S3: {e}")
        super().delete(*args, **kwargs)

