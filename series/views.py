from rest_framework import viewsets
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

class SerieViewSet(viewsets.ModelViewSet):
    queryset = Serie.objects.all().order_by('-id')
    serializer_class = SerieSerializer

class SeriesSearch(generics.ListAPIView):
    serializer_class = SerieSerializer

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return Serie.objects.filter(Q(name__icontains=query))
        else:
            return []


@api_view(['GET'])
def episode_stream(request, episode_id):
    # Obtenha o objeto Episode com base no episode_id (substitua isso com sua própria lógica)
    episode = get_object_or_404(Episode, pk=episode_id)

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