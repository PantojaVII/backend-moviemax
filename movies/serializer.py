from rest_framework import serializers
from .models import Movie


# Ao usar o atributo choices em um campo de modelo, como CharField ou IntegerField,
# você pode fornecer um conjunto de opções pré-definidas para esse campo.
# O atributo get_FOO_display() é um método gerado automaticamente pelo
# Django para campos que usam a opção choices.
# Quando você chama get_name_display(), ele retorna a representação
# amigável (human-readable) da opção de escolha associada ao valor numérico armazenado no banco de dados.

class MoviesSerializer(serializers.ModelSerializer):
    #genres = serializers.SerializerMethodField() em um serializador do Django REST Framework
    # indica que você está criando um campo personalizado chamado genres,
    # e você fornecerá a lógica para obter os dados desse campo por meio de um método chamado get_genres
    id = serializers.CharField(source='hashed_id')

    genres = serializers.SerializerMethodField()
    # para achar o modelo, o nome precisa ser igual ao da representação do
    # model no caso o 'genres'

    age_groups = serializers.SerializerMethodField()
    #é usado quando você precisa fornecer uma lógica
    # personalizada para a obtenção do valor desses campos.

    info = serializers.SerializerMethodField()



    class Meta:
        model = Movie
        exclude = ['company','hashed_id']

    def get_genres(self, obj):
        #o get_name_display é o retorno do que foi definido no model
        return [genre.get_name_display() for genre in obj.genres.all()]

    def get_info(self, obj):
        #o get_name_display é o retorno do que foi definido no model
        return [inf.get_name_display() for inf in obj.info.all()]

    def get_age_groups(self, char):
        return char.get_age_groups_display()
