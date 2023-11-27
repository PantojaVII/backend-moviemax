from django.contrib import admin
from .models import Serie, Season, Episode

# Define um método para exibir os gêneros
def Genres_Series(obj):
    genres = [str(genre) for genre in obj.genres.all()]  # Converta os valores inteiros em strings
    return ", ".join(genres)


# Define a classe de administração para o modelo Serie
@admin.register(Serie)
class SerieAdmin(admin.ModelAdmin):
    list_display = ('name', 'release_date', 'director', Genres_Series)
    list_filter = ('genres',)  # Adicione um filtro para gêneros
    search_fields = ('name', 'director')  # Adicione campos de pesquisa
    filter_horizontal = ('genres',)  # Use uma interface de seleção para gêneros

# Define a classe de administração para o modelo Season
@admin.register(Season)
class SeasonAdmin(admin.ModelAdmin):
    list_display = ('serie', 'season', 'release_date')
    list_filter = ('serie',)  # Adicione um filtro para a série associada
    search_fields = ('serie__name',)  # Adicione pesquisa por nome da série

# Define a classe de administração para o modelo Episode
@admin.register(Episode)
class EpisodeAdmin(admin.ModelAdmin):
    list_display = ('season', 'num_episode', 'name', 'duration')
    list_filter = ('season__serie', 'season')  # Adicione filtros para a série e temporada associadas
    search_fields = ('season__serie__name', 'season__season', 'name')  # Adicione pesquisa por nome da série, temporada e nome do episódio
