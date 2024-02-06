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
from django.utils import timezone
from django.utils.text import slugify
from rest_framework import generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.hashers import check_password
from .models import Profile

# Definindo uma classe de visualização (viewset) para criar usuários
class UserView2(viewsets.ModelViewSet):
    # Queryset contendo todos os usuários existentes
    queryset = User.objects.all()
    # Utilizando o serializer personalizado para usuários
    serializer_class = UserSerializer
    # Definindo permissões para permitir qualquer acesso (usuários não autenticados podem criar contas)
    permission_classes = (AllowAny,)

    # Método para criar um novo usuário, estamos sobreescrevendo o método
    def create(self, request, *args, **kwargs):
        # Criando uma instância do serializer com os dados da requisição
        serializer = self.serializer_class(data=request.data)
        # Validando os dados e levantando uma exceção em caso de erro de validação
        serializer.is_valid(raise_exception=True)
        # Adicionando o campo 'username' ao dicionário de dados validados
        username = f"{slugify(serializer.validated_data['first_name'])}_{timezone.now().strftime('%Y%m%d%H%M%S')}"
        serializer.validated_data['username'] = username
        # Lista para armazenar mensagens de erro durante a validação personalizada
        errors = []
        """ print("---------------------------")
        print("---------------------------")
        print(serializer.validated_data['username'])
        print("---------------------------")
        print("---------------------------") """
        
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
    

    def update(self, request, *args, **kwargs):
        # Obtenha a instância do usuário que está sendo atualizado
        instance = self.get_object()
        
        errors = []
        msg = []

        # Crie uma instância do serializer com os dados da requisição e a instância do usuário
        serializer = self.serializer_class(instance, data=request.data, partial=True)

        # Validando os dados e lidando com exceções em caso de erro de validação
        try:
            serializer.is_valid(raise_exception=True)
        except:
            return Response({"errors": "Dados inválidos"}, status=status.HTTP_400_BAD_REQUEST)

        # Verifique se a senha atual fornecida corresponde à senha do usuário
        if 'password' in serializer.validated_data:
            if not check_password(serializer.validated_data['password'], instance.password):
                # Senha atual fornecida não corresponde à senha do usuário

                return Response({"errors": ['Senha incorreta']}, status=status.HTTP_401_UNAUTHORIZED)

        # Se uma nova senha estiver sendo fornecida, aplique o hash antes de salvar
        if 'new_password' in serializer.validated_data:
            instance.set_password(serializer.validated_data['new_password'])
            msg.append("Senha alterada com sucesso")
        
        # Atualizando o campo first_name
        if 'first_name' in serializer.validated_data:
            instance.first_name = serializer.validated_data['first_name']
            msg.append("Nome de usuário alterado com sucesso")
        # Salvando as alterações no usuário

        instance.save()
        return Response(msg)

class CustomLogin(viewsets.GenericViewSet, ObtainAuthToken):
    serializer_class = LoginSerializer

    @action(detail=False, methods=['post'])
    def login(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        password = serializer.validated_data['password']

        try:
            validate_login_credentials(request, email, password)
            user = EmailBackend().authenticate(request, email=email, password=password)
            token, _ = Token.objects.get_or_create(user=user)
            return Response(
                {'token': token.key},
            status=status.HTTP_200_OK)
        except ValidationError as e:
            return Response({"message": e}, status=status.HTTP_401_UNAUTHORIZED)



class UserProfile(generics.ListAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        # O usuário autenticado está disponível em request.user
 
        user = request.user

        # Agora você pode acessar os atributos do usuário, como username e email
        user_data = {
            'id': user.id,
            'first_name': user.first_name,
            'email': user.email,
            # Adicione outros campos do modelo de usuário conforme necessário
        }
        return Response(user_data, status=status.HTTP_200_OK)