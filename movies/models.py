import os
from django.db import models
from genres.models import Genre, Info
import hashlib
from django.db import models
from django.conf import settings


groups = (
    (1, 'LIVRE'),
    (2, '+10'),
    (3, '+12'),
    (4, '+16'),
    (5, '+18'),
);


def movie_upload_path(instance, filename):
    # instance.id ainda não foi definido, usando UUID temporário
    return f'movies/{instance.id}/{filename}'


class Movie(models.Model):
    id = models.AutoField(primary_key=True)
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
    player = models.FileField(upload_to=movie_upload_path)
    file_size = models.PositiveIntegerField(null=True, blank=True, editable=False,default=0)
    def save(self, *args, **kwargs):

        if self.player:
            # Calcula o tamanho do arquivo em bytes
            self.file_size = self.player.size
        # Se o objeto ainda não tem um ID, isso significa que é um novo objeto
        if not self.id:
            last_movie = Movie.objects.order_by('-id').first()
            last_id = last_movie.id if last_movie else 0
            self.id = last_id + 1

        # Chame o método save() da classe pai para realizar o salvamento real
        super().save(*args, **kwargs)
    def __str__(self):
        return f'{self.name} - {self.release_date}'
