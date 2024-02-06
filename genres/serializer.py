from rest_framework import serializers
from .models import Genre

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        exclude = ['id']
    # Adiciona um campo adicional para retornar o nome do gênero
    name = serializers.CharField(source='get_name_display', read_only=True)
