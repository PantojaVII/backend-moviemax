from django.contrib import admin
from .models import Serie, Season, Episode, Info
from django import forms
import requests
from django.conf import settings
# Define um método para exibir os gêneros
endpoint_storage_episodes = settings.BASE_EPISODES_ENDPOINT
endpoint_destroy_season = settings.BASE_SEASON_DESTROY_ENDPOINT
endpoint_destroy_series = settings.BASE_SERIES_DESTROY_ENDPOINT
def Genres_Series(obj):
    genres = [str(genre) for genre in obj.genres.all()]  # Converta os valores inteiros em strings
    return ", ".join(genres)

def Info_Series(obj):
    info_list = [str(info) for info in obj.info.all()]
    return ", ".join(info_list)


# Define a classe de administração para o modelo Serie
@admin.register(Serie)
class SerieAdmin(admin.ModelAdmin):
    list_display = ('name', 'release_date', 'director', Genres_Series, Info_Series)
    list_filter = ('genres',)  # Adicione um filtro para gêneros
    search_fields = ('name', 'director')  # Adicione campos de pesquisa
    filter_horizontal = ('genres', 'info')  # Use uma interface de seleção para gêneros e info
    def get_actions(self, request):
        actions = super().get_actions(request)
        # Remover a ação padrão de exclusão em massa
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions
    actions = ['delete_selected_with_custom_logic']

    def delete_selected_with_custom_logic(self, request, queryset):
        """
        Método para exclusão em massa das temporadas selecionados, com lógica personalizada.
        """
        try:
            for serie in queryset:
                # Chamando o método delete personalizado do modelo
                serie.delete()
        except Exception as e:
            print(f"Erro ao enviar a solicitação DELETE: {e}")

        # Exclui os episódios selecionados em massa no banco de dados
        queryset.delete()
        # Mensagem de sucesso
        self.message_user(request, "Episódios selecionados foram excluídos com sucesso.")
    # Definição do nome da ação para aparecer no Admin
    delete_selected_with_custom_logic.short_description = "Excluir selecionados"

# Define a classe de administração para o modelo Season

@admin.register(Season)
class SeasonAdmin(admin.ModelAdmin):
    list_display = ('serie', 'season', 'release_date')
    list_filter = ('serie',)  # Adicione um filtro para a série associada
    search_fields = ('serie__name',)  # Adicione pesquisa por nome da série
    def get_actions(self, request):
        actions = super().get_actions(request)
        # Remover a ação padrão de exclusão em massa
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions
    actions = ['delete_selected_with_custom_logic']

    def delete_selected_with_custom_logic(self, request, queryset):
        """
        Método para exclusão em massa das temporadas selecionados, com lógica personalizada.
        """
        try:
            for season in queryset:
                # Chamando o método delete personalizado do modelo
                season.delete()
        except Exception as e:
            print(f"Erro ao enviar a solicitação DELETE: {e}")

        # Exclui os episódios selecionados em massa no banco de dados
        queryset.delete()
        # Mensagem de sucesso
        self.message_user(request, "Episódios selecionados foram excluídos com sucesso.")
    # Definição do nome da ação para aparecer no Admin
    delete_selected_with_custom_logic.short_description = "Excluir selecionados"


# Define a classe de administração para o modelo Episode
@admin.register(Episode)
class EpisodeAdmin(admin.ModelAdmin):
    list_display = ('num_episode','name','duration', 'season' )
    list_filter = ('season__serie', 'season')  # Adicione filtros para a série e temporada associadas
    search_fields = ('season__serie__name', 'season__season', 'name')  # Adicione pesquisa por nome da série, temporada e nome do episódio
    # Define o campo 'season' como clicável
    list_display_links = ('season','name', 'num_episode')
    widgets = {
        'player': forms.ClearableFileInput(attrs={'multiple': False})
    }
    def get_actions(self, request):
        actions = super().get_actions(request)
        # Remover a ação padrão de exclusão em massa
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions
    actions = ['delete_selected_with_custom_logic']
    def delete_selected_with_custom_logic(self, request, queryset):
        """
        Método para exclusão em massa das temporadas selecionados, com lógica personalizada.
        """
        try:
            for episode in queryset:
                # Chamando o método delete personalizado do modelo
                episode.delete()
        except Exception as e:
            print(f"Erro ao enviar a solicitação DELETE: {e}")

        # Exclui os episódios selecionados em massa no banco de dados
        queryset.delete()
        # Mensagem de sucesso
        self.message_user(request, "Filmes selecionados foram excluídos com sucesso.")
    # Definição do nome da ação para aparecer no Admin
    delete_selected_with_custom_logic.short_description = "Excluir selecionados"

