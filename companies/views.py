from rest_framework import viewsets
from .models import Companie
from .serializer import CompanieSerializer

class CompanieViewSet(viewsets.ModelViewSet):
    queryset = Companie.objects.all()
    serializer_class = CompanieSerializer
