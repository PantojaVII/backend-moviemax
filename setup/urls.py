from django.contrib import admin
from django.urls import path, include
from companies.views import CompanieViewSet
from movies.views import MovieViewSet, movie_stream
from series.views import SerieViewSet, episode_stream
from likes.views import LikesViewSet
from search.views import Search
from accounts.views import CreateUserView2, CustomAuthTokenViewSet
from django.conf.urls.static import static
from django.conf import settings
from rest_framework import routers

"""routers do Django REST framework, que fornece funcionalidades para criar automaticamente URLs para as 
visualizações do modelo."""

router = routers.DefaultRouter()
"""router = routers.DefaultRouter(): Criando uma instância do DefaultRouter. O DefaultRouter é um roteador que ajuda 
a gerar URLs automaticamente para as visualizações do modelo registradas. Você pode usá-lo para configurar URLs para 
operações CRUD em seus modelos, como listar, criar, atualizar e excluir registros."""
router.register('Companies', CompanieViewSet, basename='Companies')
router.register('Movies', MovieViewSet, basename='Movies')
router.register('Series', SerieViewSet, basename='Series')
router.register('Likes', LikesViewSet, basename='Likes')
router.register('Accounts', CreateUserView2, basename='Accounts')
router.register('login', CustomAuthTokenViewSet, basename='login')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('movies/stream/<int:movie_id>/', movie_stream, name='movie_stream'),
    path('episode/stream/<int:episode_id>/', episode_stream, name='episode_stream'),
    path('search/', Search.as_view(), name='media_search'),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
