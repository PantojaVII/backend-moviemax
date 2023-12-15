# Importando as classes e módulos necessários do Django REST framework
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

# Definindo uma classe de visualização (viewset) para criar usuários
class CreateUserView2(viewsets.ModelViewSet):
    # Queryset contendo todos os usuários existentes
    queryset = User.objects.all()
    # Utilizando o serializer personalizado para usuários
    serializer_class = UserSerializer
    # Definindo permissões para permitir qualquer acesso (usuários não autenticados podem criar contas)
    permission_classes = (AllowAny,)

    # Método para criar um novo usuário
    def create(self, request, *args, **kwargs):
        # Criando uma instância do serializer com os dados da requisição
        serializer = self.serializer_class(data=request.data)
        # Validando os dados e levantando uma exceção em caso de erro de validação
        serializer.is_valid(raise_exception=True)

        # Lista para armazenar mensagens de erro durante a validação personalizada
        errors = []

        # Validando a unicidade do endereço de e-mail
        try:
            validate_unique_email(serializer.validated_data['email'])
        except ValidationError as e:
            error_message = str(e).strip("[]").replace("'", "")
            errors.append(error_message)

        # Validando a confirmação de senha
        try:
            validate_password_confirmation(
                serializer.validated_data['password'], serializer.validated_data['password_confirmation'])
        except ValidationError as e:
            error_message = str(e).strip("[]").replace("'", "")
            errors.append(error_message)



        # Se houver erros, retornar uma resposta de erro com as mensagens
        if errors:
            return Response({"errors": errors}, status=status.HTTP_401_UNAUTHORIZED)

        # Removendo 'password_confirmation' do dicionário de dados validados
        validated_data = serializer.validated_data
        validated_data.pop('password_confirmation', None)

        # Criando o usuário no banco de dados usando o método 'create_user' do modelo User
        user = User.objects.create_user(**validated_data)

        # Gerando e associando um token ao usuário recém-criado
        Token.objects.create(user=user)

        # Obtendo os cabeçalhos de sucesso e retornando uma resposta com status 201 (criado)
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
