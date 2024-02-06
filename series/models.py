import os
from django.db import models
from genres.models import Genre, Info
from companies.models import Companie
from django.conf import settings
from utils.common import generate_hash

groups = (
    (1, 'LIVRE'),
    (2, '+10'),
    (3, '+12'),
    (4, '+16'),
    (5, '+18'),
);
def movie_upload_path(instance, filename):
    return f'series/{instance.id}/{filename}'
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
        media_root = settings.MEDIA_ROOT
        # Crie o diretório da temporada
        season_folder = os.path.join(media_root, f'series/{self.serie.id}/Season {self.season}')
        try:
            os.makedirs(season_folder, exist_ok=True)
            print(f"Diretório criado com sucesso: {season_folder}")
        except Exception as e:
            print(f"Erro ao criar o diretório: {e}")
class Episode(models.Model):
    season = models.ForeignKey(Season, on_delete=models.CASCADE, related_name='episodes')
    hashed_id = models.CharField(max_length=64, blank=True, null=True, unique=True)  
    num_episode  = models.PositiveSmallIntegerField()  # numero episode   
    name = models.CharField(max_length=100)  # Nome do episódio
    duration = models.DurationField()  # Duração do episódio
    synopsis = models.TextField()
    player = models.FileField(upload_to=episode_upload_path)
    created_at = models.DateTimeField(auto_now_add=True)  # Data e hora de criação do registro
    updated_at = models.DateTimeField(auto_now=True)  # Data e hora da última atualização
    file_size = models.PositiveIntegerField(null=True, blank=True, editable=False,default=0)
    def __str__(self):
        return f"{self.season} - Episódio {self.name}"

    def save(self, *args, **kwargs):
        if not self.hashed_id:
            self.hashed_id = generate_hash()
        if self.player:
            # Calcula o tamanho do arquivo em bytes
            self.file_size = self.player.size
        # Se o objeto já existe (possui um ID), exclua o arquivo antigo antes de salvar o novo
        if self.id:
            old_episode = Episode.objects.get(id=self.id)
            if old_episode.player:
                # Exclua o arquivo antigo
                old_file_path = os.path.join(settings.MEDIA_ROOT, str(old_episode.player))
                if os.path.exists(old_file_path):
                    os.remove(old_file_path)

        # Chame o método save() da classe pai para realizar o salvamento real
        super().save(*args, **kwargs)

        def delete(self, *args, **kwargs):
            # Exclua o arquivo associado ao campo player
            if self.player:
                file_path = os.path.join(settings.MEDIA_ROOT, str(self.player))
                if os.path.exists(file_path):
                    os.remove(file_path)

            # Chame o método delete() da classe pai para realizar a exclusão real
            super().delete(*args, **kwargs)

