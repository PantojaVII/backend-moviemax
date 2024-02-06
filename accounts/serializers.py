# serializers.py
from django.contrib.auth.models import User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    password_confirmation = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ('first_name', 'email', 'password', 'password_confirmation', "new_password")
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, data):

        return data


# serializers.py
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):

        return data
