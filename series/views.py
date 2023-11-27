from rest_framework import viewsets
from .models import Serie
from .serializer import SerieSerializer

class SerieViewSet(viewsets.ModelViewSet):
    queryset = Serie.objects.all()
    serializer_class = SerieSerializer
