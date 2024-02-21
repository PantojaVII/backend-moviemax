from django.contrib import admin
from django.utils.html import format_html
from django.contrib import messages
from .models import Movie, Genre, Info

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Info)
class InfoAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('name', 'release_date', 'director', 'display_player')
    list_filter = ('genres',)
    search_fields = ('name', 'director')
    filter_horizontal = ('genres', 'info')
    actions = ['delete_selected']

    def display_player(self, obj):
        # Exibe um link para o arquivo player (se estiver presente)
        if obj.player:
            return format_html(f'<a href="{obj.player.url}" target="_blank">Ver Player</a>')
        return '-'

    display_player.short_description = 'Player'
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
            for movie in queryset:
                # Chamando o método delete personalizado do modelo
                movie.delete()
        except Exception as e:
            print(f"Erro ao enviar a solicitação DELETE: {e}")

        # Exclui os episódios selecionados em massa no banco de dados
        queryset.delete()
        # Mensagem de sucesso
        self.message_user(request, "Episódios selecionados foram excluídos com sucesso.")
    # Definição do nome da ação para aparecer no Admin
    delete_selected_with_custom_logic.short_description = "Excluir selecionados"
