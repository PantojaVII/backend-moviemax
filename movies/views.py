from rest_framework import viewsets, filters
from .models import Movie
from .serializer import MoviesSerializer
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.http import StreamingHttpResponse
from django.http import HttpResponse
from django.core.exceptions import SuspiciousOperation
import time
import mimetypes
import os
from time import sleep
class GenreFilter(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        genre_id = request.query_params.get('genre')
        if genre_id:
            return queryset.filter(genres__id=genre_id)
        return queryset.filter(genres__id=genre_id).distinct()
   
    
class MovieViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    queryset = Movie.objects.all().order_by('-id')
    serializer_class = MoviesSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = [
        'name', 
        'genres__hashed_id',
        'synopsis',
        "release_date",
        "rating",
        'hashed_id'
    ]
    # Adicione a classe de paginação
     
    
    def get_queryset(self):
        movie_id = self.request.query_params.get('movie', None)
        search_param = self.request.query_params.get('search', None)
        search_field_param = self.request.query_params.get('content', None)
        
        if movie_id:
            queryset = Movie.objects.filter(hashed_id=movie_id)
        elif search_param and search_field_param:
            if search_field_param == "genres":
                filter_kwargs = {f'{search_field_param}__hashed_id': search_param}
                queryset = Movie.objects.filter(**filter_kwargs)
            else:
                filter_kwargs = {f'{search_field_param}__icontains': search_param}
                queryset = Movie.objects.filter(**filter_kwargs)
                
        else:
            queryset = self.queryset

            if search_field_param == 'rating':
                queryset = queryset.order_by('-rating')

        return queryset

@api_view(['GET'])
def movie_stream(request, movie_hash):
    # Obtendo o objeto Movie com base no hashed_id fornecido, ou retornando um erro 404 se não encontrado
    movie = get_object_or_404(Movie, hashed_id=movie_hash)
    video_size = movie.file_size

    # Calculando a duração total do vídeo em segundos
    duration_in_seconds = movie.duration.total_seconds()

    # Calculando bytes por segundo
    bytes_per_second = video_size / duration_in_seconds

    # Calculando o intervalo desejado em bytes para 30 segundos
    interval_bytes = int(bytes_per_second) * 120

    # Obtendo o caminho do vídeo do objeto Movie, ou definindo como None se não houver
    video_path = movie.player.path if movie.player else None

    # Verificando se o cabeçalho Range está presente na requisição
    if 'Range' in request.headers:
        range_header = request.headers['Range']
        # O cabeçalho Range tem o formato 'bytes=start-end'
        # Aqui vamos dividir o cabeçalho e pegar o valor de start
        start_byte = int(range_header.split('=')[1].split('-')[0])
        # Definindo o fim do intervalo como start_byte + interval_bytes
        end_byte = min(start_byte + interval_bytes, video_size - 1)  # Certifique-se de não ultrapassar o tamanho do arquivo

        # Lendo apenas a parte do vídeo especificada pelo intervalo
        with open(video_path, 'rb') as video_file:
            video_file.seek(start_byte)
            video_data = video_file.read(end_byte - start_byte + 1)

        # Retornando a parte do vídeo como resposta
        response = HttpResponse(video_data, content_type='video/mp4')
        response['Content-Length'] = len(video_data)
        response['Content-Range'] = f'bytes {start_byte}-{end_byte}/{video_size}'
        response.status_code = 206  # Status de resposta parcial

        return response

    else:
        # Se não houver cabeçalho Range na requisição, retorna o arquivo de vídeo completo
        return FileResponse(open(video_path, 'rb'), content_type='video/mp4')

