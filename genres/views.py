from django.shortcuts import render
from rest_framework import viewsets
from .models import Genre
from .serializer import GenreSerializer
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination

""" Caso queira personalizar a quantidade de paginação """
class CustomPageNumberPagination(PageNumberPagination):
    page_size = 100  # Defina o tamanho da página desejado aqui
    page_size_query_param = 'page_size'
    max_page_size = 1000  # Defina o tamanho máximo da página, se necessário

class GenreViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    pagination_class = None  # Adicione esta linha caso não queira paginação
    # Define uma ação personalizada chamada by_name
    @action(detail=False, methods=['GET'])
    def Name(self, request, *args, **kwargs):
        # Obtém o parâmetro 'name' da query string da requisição
        name = self.request.query_params.get('name', None)

        # Verifica se o parâmetro 'name' foi fornecido
        if name is None:
            return Response({'error': 'Parameter "name" is required'}, status=400)

        # Encontra o ID do gênero com base no nome fornecido
        """ next(..., None): next é uma função que obtém o próximo item de um iterador. No caso, ela recebe a expressão geradora definida anteriormente como primeiro argumento. O segundo argumento, None, é um valor padrão a ser retornado caso o iterador esteja vazio. """
        genre_id = next((id for id, genre_name in Genre.GENRE_CHOICES if genre_name == name), None)

        # Verifica se o genre_id foi encontrado
        if genre_id is not None:
            try:
                # Tenta buscar o objeto Genre pelo genre_id
                genre = Genre.objects.get(name=genre_id)
                # Serializa o objeto encontrado
                serializer = self.get_serializer(genre)
                # Retorna os dados serializados como resposta
                return Response(serializer.data)
            except Genre.DoesNotExist:
                # Retorna um erro indicando que o gênero não foi encontrado
                return Response({'error': 'Genre not found'}, status=404)
        else:
            # Retorna um erro indicando que o nome do gênero fornecido é inválido
            return Response({'error': 'Invalid genre name'}, status=400)
    
