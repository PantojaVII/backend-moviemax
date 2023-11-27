from rest_framework import viewsets
from .models import Likes
from .serializer import LikesSerializer

class LikesViewSet(viewsets.ModelViewSet):
    queryset = Likes.objects.all()
    serializer_class = LikesSerializer
