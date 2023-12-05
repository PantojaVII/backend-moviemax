from rest_framework import viewsets
from .models import Movie
from .serializer import MoviesSerializer
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.http import StreamingHttpResponse
from django.http import HttpResponse, HttpResponseBadRequest
from django.utils.http import http_date
import mimetypes
import os
import re
class MovieViewSet(viewsets.ModelViewSet):
   # permission_classes = [IsAuthenticatedOrPostOnly]
    queryset = Movie.objects.all().order_by('-id')
    serializer_class = MoviesSerializer


@api_view(['GET'])
def movie_stream(request, movie_id):
    try:
        # Obtém o objeto Movie pelo ID usando a função get_object_or_404
        movie = get_object_or_404(Movie, pk=movie_id)
        # Obtém o caminho do vídeo a partir do campo 'player' do objeto Movie
        video_path = movie.player.path

        # Obtenha o tamanho total do arquivo
        total_size = movie.file_size

        # Define uma função de geração para transmitir o conteúdo do arquivo
        def file_iterator(file_path, start_byte=0, end_byte=None, chunk_size=8192):
            with open(file_path, 'rb') as f:
                # Se um intervalo é especificado, ajuste a posição do arquivo
                if start_byte > 0:
                    f.seek(start_byte)
                else:
                    start_byte = f.tell()

                remaining_bytes = end_byte - start_byte + 1 if end_byte else None

                while remaining_bytes is None or remaining_bytes > 0:
                    # Leia o próximo chunk ou até o final do intervalo
                    chunk = f.read(min(chunk_size, remaining_bytes))
                    if not chunk:
                        break
                    yield chunk

                    if remaining_bytes:
                        remaining_bytes -= len(chunk)

        # Verifica se o cabeçalho 'Range' está presente na solicitação
        if 'Range' in request.headers:
            # Obtém o valor do cabeçalho 'Range'
            range_header = request.headers['Range']

            # Usa uma expressão regular para extrair as informações de intervalo
            match = re.match(r'bytes=(\d+)-(\d*)', range_header)

            if match:
                # Obtém o ponto inicial do intervalo
                start_byte = int(match.group(1))

                # Obtém o ponto final do intervalo, se fornecido; caso contrário, usa o tamanho total do arquivo
                end_byte = int(match.group(2)) if match.group(2) else total_size - 1

                # Verifica se o intervalo está dentro dos limites do arquivo
                if start_byte >= total_size or end_byte >= total_size:
                    return HttpResponseBadRequest("Intervalo solicitado fora do alcance do arquivo.")

                # Calcula o tamanho do chunk (pedaço) a ser enviado como resposta
                chunk_size = 19663 if end_byte is None else end_byte - start_byte + 1

                # Gera um iterador de arquivo usando a função file_iterator ajustada
                file_iter = file_iterator(video_path, start_byte, end_byte, chunk_size)

                # Cria uma resposta de streaming com status 206 (206 Partial Content)
                response = StreamingHttpResponse(file_iter, status=206)

                # Adiciona cabeçalhos necessários para indicar o conteúdo parcial e informações sobre o intervalo
                response['Content-Type'] = 'video/mp4'
                response['Content-Range'] = f'bytes {start_byte}-{end_byte}/{total_size}'


                # Retorna a resposta com o conteúdo parcial
                return response

        response = HttpResponseBadRequest("Sem cabeçalho 'Range' na solicitação")
        response['Content-Type'] = 'video/mp4'
        return response

    except FileNotFoundError:
        return Response({'error': 'Arquivo de vídeo não encontrado'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        print(f"Erro ao abrir o arquivo de vídeo: {str(e)}")
        return Response({'error': 'Erro ao processar o vídeo'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


