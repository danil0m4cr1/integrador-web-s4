from rest_framework import serializers

from .models import (
    Categoria, 
    Laboratorio,
    Ativo,
    Usuario,
    Movimentacao,
    OrdemServico
)

from django.contrib.auth.models import User

# Cadastro de Usuario Serializer
class CadastroUsuarioSerializers(serializers.Serializer):
    password = serializers.CharField(write_only = True)
    nome = serializers.CharField()
    email = serializers.EmailField()
    telefone = serializers.CharField(
        required = False,
        allow_blank = True
    )

    def validated_username(self, value):
        if User.objects.filter(username = value).exists():
            raise serializers.ValidationError(
                "Este nome de usuário já está cadastrado"
            )
        
        return value

    def validate_email(self, value):
        if User.objects.filter(email = value).exists():
            raise serializers.ValidationError(
                "Este email já está cadastrado"
            )
        return value

    def create(self, validated_data):
        # Criando o usuario de autenticacao do django
        usuario = Usuario.objects.create_user(
            username = validated_data['username'],
            email = validated_data['email'],
            password = validated_data['password']
        )

        return usuario

    def to_representation(self, instance):
        return {
            "id": instance.id,
            "username": instance.usuario.username,
            "nome": instance.nome,
            "email": instance.email,
            "telefone": instance.telefone
        }

# Categoria Serializer
class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = "__all__"

# Laboratorio Serializer
class LaboratorioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Laboratorio
        fields = "__all__"
        

# Ativo Serializer
class AtivoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ativo
        fields = "__all__"

# Movimentacao Serializer
class MovimentacaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movimentacao
        fields = "__all__"

# OrdemServico Serializer
class OrdemServicoSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrdemServico
        fields = [
            "ativo",
            "usuario",
            "descricao",
            "status"
        ]