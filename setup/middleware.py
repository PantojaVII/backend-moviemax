from rest_framework.authtoken.models import Token
from utils.common import validate_date
 
class PrintMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Extrai o token do cabeçalho Authorization, se estiver presente
        authorization_header = request.headers.get('Authorization', '')
        if authorization_header.startswith('Token '):
            token_key = authorization_header.split(' ')[1]
            try:
                token = Token.objects.get(key=token_key)
                user = token.user
                response = validate_date(user)
                if response:
                    return response
            except Token.DoesNotExist:
                print(f"Token inválido: {token_key}")
        else:
            print("Nenhum token presente no cabeçalho Authorization")

        response = self.get_response(request)
        return response
