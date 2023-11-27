from django.db import models

# Modelo para as categorias dos filmes
class Genre(models.Model):
    #uma tupla
    GENRE_CHOICES = (
        (1, 'Ação'),
        (2, 'Aventura'),
        (3, 'Cinema de arte'),
        (4, 'Chanchada'),
        (5, 'Comédia'),
        (6, 'Comédia romântica'),
        (7, 'Dança'),
        (8, 'Documentário'),
        (9, 'Drama'),
        (10, 'Espionagem'),
        (11, 'Fantasia'),
        (12, 'Ficção científica'),
        (13, 'Guerra'),
        (14, 'Mistério'),
        (15, 'Musical'),
        (16, 'Policial'),
        (17, 'Romance'),
        (18, 'Terror'),
    )
    name = models.PositiveSmallIntegerField(choices=GENRE_CHOICES, default=1, unique=True)

    def __str__(self):
        return dict(self.GENRE_CHOICES)[self.name]


class Info(models.Model):
    groups_Info  = (
        (1, 'FILME'),
        (2, 'SERIE'),
        (3, 'Heróis'),
        (4, 'Marvel'),
        (5, 'DC'),
        (6, 'HD'),
        (7, 'FullHd'),
    )
    name = models.PositiveSmallIntegerField(choices=groups_Info, default=1, unique=True)

    def __str__(self):
        return dict(self.groups_Info)[self.name]

