from rest_framework import viewsets
from .models import Movie
from .serializer import MoviesSerializer
from .permissions import IsAuthenticatedOrPostOnly  # Importe sua classe de permissão personalizada

class MovieViewSet(viewsets.ModelViewSet):
   # permission_classes = [IsAuthenticatedOrPostOnly]
    queryset = Movie.objects.all().order_by('-id')
    serializer_class = MoviesSerializer

