from rest_framework import serializers
from .models import Likes

class LikesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Likes
        fields = ('type', 'content_id')
