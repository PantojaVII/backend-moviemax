from rest_framework import viewsets, filters
from .models import Movie
from .serializer import MoviesSerializer
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from django.http import StreamingHttpResponse, HttpResponse
from django.utils.http import http_date
import os
from rest_framework import generics
from django.db.models import Q
 

class GenreFilter(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        genre_id = request.query_params.get('genre')
        if genre_id:
            return queryset.filter(genres__id=genre_id)
        return queryset.filter(genres__id=genre_id).distinct()
class MovieViewSet(viewsets.ModelViewSet):
   # permission_classes = [IsAuthenticatedOrPostOnly]
    queryset = Movie.objects.all().order_by('-id')
    serializer_class = MoviesSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'director', 'genre']  # Adicione campos pelos quais você deseja realizar pesquisa
   # movies/?search=nome_do_filme

class MoviesSearch(generics.ListAPIView):
    serializer_class = MoviesSerializer

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return Movie.objects.filter(Q(name__icontains=query))
        else:
            return []
@api_view(['GET'])
def movie_stream(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    video_path = movie.player.path
    video_size = movie.file_size

    if os.path.exists(video_path):
        range_header = request.headers.get('Range')
        start_byte = int(range_header.split('=')[-1].split('-')[0]) if range_header else 0
        end_byte = video_size - 1

        with open(video_path, 'rb') as video_file:
            video_file.seek(start_byte)
            content = video_file.read(end_byte - start_byte)

        response = HttpResponse(content, content_type='video/mp4')
        response['Accept-Ranges'] = 'bytes'
        response['Content-Range'] = f'bytes {start_byte}-{end_byte - 1}/{video_size}'

        return response
    else:
        return HttpResponse('O vídeo não foi encontrado.', status=404)
