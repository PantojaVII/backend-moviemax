from rest_framework import serializers
from genres.models import Genre
from .models import Serie, Season, Episode

class EpisodeSerializer(serializers.ModelSerializer):
    id = serializers.CharField(source='hashed_id')
    class Meta:
        model = Episode
        fields = (
            'id',
            'num_episode',
            'name',
            'duration',
            'player',
            'file_size'
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
    age_groups = serializers.SerializerMethodField()
    info = serializers.SerializerMethodField()
    id = serializers.CharField(source='hashed_id')
    
    class Meta:
        model = Serie
        exclude = ['company', 'hashed_id']

    def get_genres(self, obj):
        #o get_name_display é o retorno do que foi definido no model
        return [genre.get_name_display() for genre in obj.genres.all()]

    def get_age_groups(self, char):
        return char.get_age_groups_display()
    def get_info(self, obj):
        #o get_name_display é o retorno do que foi definido no model
        return [inf.get_name_display() for inf in obj.info.all()]