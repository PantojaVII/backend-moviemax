from django.contrib import admin
from companies.models import Companie

class CompanieAdmin(admin.ModelAdmin):
        list_display = ('id', 'name', 'cnpj', 'address', 'email', 'phoneNumber')
        list_display_links = ('id', 'name')#posso clicar nesses 2 que vai abrir 
        search_fields = ('cnpj', 'name')
        list_per_page = 20

admin.site.register(Companie, CompanieAdmin)