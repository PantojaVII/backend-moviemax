from rest_framework import viewsets, filters
from .models import Serie, Episode
from .serializer import SerieSerializer
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
from django.http import StreamingHttpResponse
from django.http import HttpResponse, HttpResponseBadRequest
import re
import os
from django.core.files import File
from rest_framework import generics
from django.db.models import Q


class GenreFilter(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        genre_id = request.query_params.get('genre')
        if genre_id:
            return queryset.filter(genres__id=genre_id)
        return queryset.filter(genres__id=genre_id).distinct()
 
class SerieViewSet(viewsets.ModelViewSet):
    queryset = Serie.objects.all().order_by('-id')
    serializer_class = SerieSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter] #bibliotecas de ordenação
    search_fields = [
        'name', 
        'genres__hashed_id',
        'synopsis',
        "release_date",
        "rating"
        ]
    #campos de busca
    # movies/?search=nome_do_filme => exempo de busca
    
    def get_queryset(self):
        
        serie_id = self.request.query_params.get('serie', None)
        search_param = self.request.query_params.get('search', None)
        search_field_param = self.request.query_params.get('content', None)
            
        if serie_id:
            queryset = Serie.objects.filter(hashed_id=serie_id)
        elif search_param and search_field_param:
            if search_field_param == "genres":  # Corrigido para usar == em vez de is
                filter_kwargs = {f'{search_field_param}__hashed_id': search_param}
                queryset = Serie.objects.filter(**filter_kwargs)
            else:
                print('aqui')
                filter_kwargs = {f'{search_field_param}__icontains': search_param}
                queryset = Serie.objects.filter(**filter_kwargs)
                
        else:
            queryset = self.queryset

            if search_field_param == 'rating':
                queryset = queryset.order_by('-rating')

        return queryset


@api_view(['GET'])
def episode_stream(request, episode):

    episode = get_object_or_404(Episode, hashed_id=episode)
    video_size = episode.file_size
    # Calculando a duração total do vídeo em segundos
    duration_in_seconds = episode.duration.total_seconds()

    # Calculando bytes por segundo
    bytes_per_second = video_size / duration_in_seconds

    # Calculando o intervalo desejado em bytes para 30 segundos
    interval_bytes = int(bytes_per_second) * 120

    # Obtendo o caminho do vídeo do objeto Movie, ou definindo como None se não houver
    video_path = episode.player.path if episode.player else None

    # Obtendo o caminho do vídeo do objeto Movie, ou definindo como None se não houver
    video_url = episode.playerURL if episode.playerURL else None

    if video_url:
        return JsonResponse({'MESSAGE': 'EXTERNAL URL'})

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


    

