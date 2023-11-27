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

    def delete_selected(modeladmin, request, queryset):
        # Implemente a lógica de exclusão aqui
        # Certifique-se de tratar erros e exibir mensagens de sucesso

        # Exemplo básico:
        try:
            count = queryset.count()
            queryset.delete()
            messages.success(request, f'{count} filmes foram excluídos com sucesso.')
        except Exception as e:
            messages.error(request, f'Ocorreu um erro ao excluir os filmes: {str(e)}')

    delete_selected.short_description = 'Excluir filmes selecionados'
