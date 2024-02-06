# movies/views.py
from rest_framework import generics
from django.db.models import Q
from movies.models import Movie
from series.models import Serie
from movies.serializer import MoviesSerializer
from series.serializer import SerieSerializer


class Search(generics.ListAPIView):
    serializer_class = SerieSerializer  # Você pode ajustar isso conforme necessário

    def get_queryset(self):
        query = self.request.GET.get('q')
        print(query)
        if query:
            # Consulta tanto filmes quanto séries com base no nome
            movies_query = Movie.objects.filter(Q(name__icontains=query))
            series_query = Serie.objects.filter(Q(name__icontains=query))

            # Combine os resultados em uma lista
            search_results = list(movies_query) + list(series_query)
            return search_results
        else:
            return false

class SearchGenre(generics.ListAPIView):
    serializer_class = SerieSerializer  # Você pode ajustar isso conforme necessário

    def get_queryset(self):
        genre = self.request.GET.get('genre')  # Adicione a obtenção do parâmetro 'genre'
        
        if genre:
            # Consulta tanto filmes quanto séries com base no gênero
            movies_query = Movie.objects.filter(genres__id=genre)
            series_query = Serie.objects.filter(genres__id=genre)

            # Combine os resultados em uma lista
            search_results = list(movies_query) + list(series_query)

            return search_results
        else:
            return []
