from django.db import models

class Likes(models.Model):
    TYPE_CHOICES = (
        (1, 'Filme'),
        (2, 'Série'),
    )

    type = models.PositiveSmallIntegerField(choices=TYPE_CHOICES)
    content_id = models.PositiveIntegerField()

    def __str__(self):
        return f"Like #{self.id} - Tipo: {dict(self.TYPE_CHOICES)[self.type]}, ID: {self.content_id}"
