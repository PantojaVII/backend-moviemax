from rest_framework import serializers
from .models import Companie

class CompanieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Companie
        fields = '__all__'
