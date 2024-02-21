from django.contrib.auth.models import User
from django.contrib import admin
from .models import Profile

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'user_email', 'date_block')  # Adiciona 'user_email' em list_display
    search_fields = ('user__username', 'user__email', 'date_block')  # Adiciona 'user__email' em search_fields
    list_display_links = ('user', 'user_email')
    def user_email(self, obj):
        return obj.user.email

    user_email.short_description = 'Email do Usuário'  # Define o cabeçalho da coluna

