#views
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import viewsets, status
from rest_framework.permissions import AllowAny
from .serializers import UserSerializer, LoginSerializer
from rest_framework.authtoken.models import Token
from .validators import *
from django.core.exceptions import ValidationError
from .backends.backends import EmailBackend


class CreateUserView2(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        errors = []

        try:
            validate_unique_email(serializer.validated_data['email'])
        except ValidationError as e:
            error_message = str(e).strip("[]").replace("'", "")
            errors.append(error_message)

        try:
            validate_password_confirmation(
                serializer.validated_data['password'], serializer.validated_data['password_confirmation'])
        except ValidationError as e:
            error_message = str(e).strip("[]").replace("'", "")
            errors.append(error_message)

        try:
            validate_lowercase_username(serializer.validated_data['username'])
        except ValidationError as e:
            error_message = str(e).strip("[]").replace("'", "")
            errors.append(error_message)

        if errors:
            return Response({"errors": errors}, status=status.HTTP_401_UNAUTHORIZED)

        validated_data = serializer.validated_data
        validated_data.pop('password_confirmation', None)  # Remova 'password_confirmation' do validated_data

        # Criando o usuário
        user = User.objects.create_user(**validated_data)

        # Gerando e associando um token ao usuário
        Token.objects.create(user=user)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class CustomAuthTokenViewSet(viewsets.GenericViewSet, ObtainAuthToken):
    serializer_class = LoginSerializer

    @action(detail=False, methods=['post'])
    def login(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        password = serializer.validated_data['password']

        try:
            validate_login_credentials(request, email, password)
        except ValidationError as e:
            return Response({"message": e}, status=status.HTTP_401_UNAUTHORIZED)

        user = EmailBackend().authenticate(request, email=email, password=password)
        token, _ = Token.objects.get_or_create(user=user)

        return Response(
            {'token': token.key},
            status=status.HTTP_200_OK)
