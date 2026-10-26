from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import viewsets, generics
from .models import (
    Usuario, 
    Categoria, 
    Laboratorio, 
    Ativo, 
    Movimentacao, 
    OrdemServico
)
from .serializers import (
    CadastroUsuarioSerializers,
    UsuarioSerializer,
    CategoriaSerializer, 
    LaboratorioSerializer, 
    AtivoSerializer, 
    MovimentacaoSerializer, 
    OrdemServicoSerializer
)
from rest_framework.permissions import (AllowAny, IsAuthenticated, IsAdminUser)
from django.http import HttpResponse
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

def home(request):
    return HttpResponse("Django Teste - Projeto Integrador")

class CadastroUsuarioViewSet(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = CadastroUsuarioSerializers
    permission_classes = [AllowAny]

class UsuarioViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all().order_by("-id")
    serializer_class = UsuarioSerializer

class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all().order_by("-id")
    serializer_class = CategoriaSerializer

class LaboratorioViewSet(viewsets.ModelViewSet):
    queryset = Laboratorio.objects.all().order_by("-id")
    serializer_class = LaboratorioSerializer

class AtivoViewSet(viewsets.ModelViewSet):
    queryset = Ativo.objects.all().order_by("-id")
    serializer_class = AtivoSerializer

class MovimentacaoViewSet(viewsets.ModelViewSet):
    queryset = Movimentacao.objects.all().order_by("-id")
    serializer_class = MovimentacaoSerializer

class OrdemServicoViewSet(viewsets.ModelViewSet):
    queryset = OrdemServico.objects.all().order_by("-id")
    serializer_class = OrdemServicoSerializer

@api_view(['POST'])
def login_usuario(request):
    email = request.data.get('email', '').strip().lower()
    password = request.data.get('password', '')

    if not email or not password:
        return Response(
            {'detail': 'Informe o e-mail e a senha.'},
            status=status.HTTP_400_BAD_REQUEST
        )

    usuario = authenticate(
        request,
        username=email,
        password=password
    )

    if usuario is None:
        return Response(
            {'detail': 'E-mail ou senha inválidos.'},
            status=status.HTTP_401_UNAUTHORIZED
        )

    return Response({
        'id': usuario.id,
        'email': usuario.email,
        'detail': 'Login realizado com sucesso.'
    }, status=status.HTTP_200_OK)
