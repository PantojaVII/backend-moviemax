from django.contrib import admin
from django.urls import path, include
from companies.views import CompanieViewSet
from movies.views import MovieViewSet, movie_stream
from series.views import SerieViewSet, episode_stream 
from genres.views import GenreViewSet
from likes.views import LikesViewSet
from search.views import Search
from accounts.views import UserView2, CustomLogin, UserProfile
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
router.register('Genres', GenreViewSet)
router.register('Likes', LikesViewSet, basename='Likes')
router.register('Accounts', UserView2, basename='Accounts')
router.register('login', CustomLogin, basename='login')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('movies/stream/<str:movie_hash>/', movie_stream, name='movie_stream'),
    path('episode/stream/<str:episode>/', episode_stream, name='episode_stream'),
    path('search/', Search.as_view(), name='media_search'),
    path('userProfile/', UserProfile.as_view(), name='user_profile'),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
