from django.db import models
from genres.models import Genre

class Serie(models.Model):
    name = models.CharField(max_length=100)
    synopsis = models.TextField()
    release_date = models.DateField()
    director = models.CharField(max_length=100)
    genres = models.ManyToManyField(Genre)
    company = models.ForeignKey('companies.Companie', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Season(models.Model):
    serie = models.ForeignKey('series.Serie', on_delete=models.CASCADE)   
    season = models.PositiveSmallIntegerField()  # temporada   
    synopsis = models.TextField()
    release_date = models.DateField()  # Data de lançamento da temporada
    created_at = models.DateTimeField(auto_now_add=True)  # Data e hora de criação do registro
    updated_at = models.DateTimeField(auto_now=True)  # Data e hora da última atualização

    def __str__(self):
        return f"{self.serie} - Temporada {self.season}"

class Episode(models.Model):

    season = models.ForeignKey('series.Season', on_delete=models.CASCADE, related_name='episodes')  
    num_episode  = models.PositiveSmallIntegerField()  # numero episode   
    name = models.CharField(max_length=100)  # Nome do episódio
    duration = models.DurationField()  # Duração do episódio
    synopsis = models.TextField()
     # URL dos players onde o episode está
    player = models.URLField()

    created_at = models.DateTimeField(auto_now_add=True)  # Data e hora de criação do registro
    updated_at = models.DateTimeField(auto_now=True)  # Data e hora da última atualização

    def __str__(self):
        return f"{self.season} - Episódio {self.name}"