from rest_framework import serializers
from genres.models import Genre
from .models import Serie, Season, Episode

class EpisodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Episode
        fields = (
             'name',
            'duration',
        )
class SeasonSerializer(serializers.ModelSerializer):
    episodes = EpisodeSerializer(many=True, read_only=True)
    class Meta:
        model = Season
        fields = (
            'season',
            'synopsis',
            'episodes',
 
        )

class SerieSerializer(serializers.ModelSerializer):
    genres = serializers.SerializerMethodField()
    season_set = SeasonSerializer(many=True, read_only=True)

    class Meta:
        model = Serie
        fields = (
            'name',
            'synopsis',
            'release_date',
            'director',
            'genres',
            'season_set',
        )

    def get_genres(self, obj):
        #o get_name_display é o retorno do que foi definido no model
        return [genre.get_name_display() for genre in obj.genres.all()]
