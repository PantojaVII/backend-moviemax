from rest_framework import viewsets, filters
from .models import Serie, Episode
from .serializer import SerieSerializer
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
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
    # Obtenha o objeto Episode com base no episode_id (substitua isso com sua própria lógica)
    episode = get_object_or_404(Episode, hashed_id=episode)
    # Caminho para o arquivo de vídeo no sistema de arquivos
    video_path = episode.player.path

    # Abra o arquivo de vídeo
    with open(video_path, 'rb') as video_file:
        video_size = episode.file_size
        response = HttpResponse()
        response['Content-Type'] = 'video/mp4'

        # Verifique se o cabeçalho 'Range' está presente na solicitação
        if 'Range' in request.headers:
            # Se o cabeçalho 'Range' estiver presente, transmita apenas a parte solicitada do vídeo
            range_header = request.headers['Range']
            start, end = process_range_header(range_header, video_size)

            # Configurar os cabeçalhos para transmitir apenas a parte solicitada
            response['Content-Range'] = f'bytes {start}-{end}/{video_size}'
            response['Content-Length'] = end - start + 1
            response.status_code = 206  # Código de status parcial

            # Lógica para posicionar o cursor no arquivo e enviar a parte correta do vídeo
            video_file.seek(start)
            response.write(video_file.read(end - start + 1))

        else:
            # Se o cabeçalho 'Range' não estiver presente, transmita o vídeo completo
            video_file = File(video_file)
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(video_path)
            response['Content-Length'] = video_size
            response.write(video_file.read())

    return response

def process_range_header(range_header, video_size):
    # Verifique se o cabeçalho 'Range' está vazio ou não está no formato esperado
    if not range_header or '=' not in range_header:
        # Se estiver vazio ou não no formato esperado, retorne o range completo
        return 0, video_size - 1

    try:
        # Tente analisar os valores do cabeçalho 'Range'
        start, end = map(int, range_header.split('=')[1].split('-'))

        # Certifique-se de que os valores estejam dentro dos limites do arquivo de vídeo
        start = min(max(0, start), video_size - 1)
        end = min(end, video_size - 1)

        return start, end
    except ValueError:
        # Se ocorrer um erro ao converter para int, retorne o range completo
        return 0, video_size - 1
    

