from django.shortcuts import render
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
    CategoriaSerializer, 
    LaboratorioSerializer, 
    AtivoSerializer, 
    MovimentacaoSerializer, 
    OrdemServicoSerializer
)
from rest_framework.permissions import (AllowAny, IsAuthenticated)
from django.http import HttpResponse

def home(request):
    return HttpResponse("Django Teste - Projeto Integrador")

class CadastroUsuarioViewSet(generics.CreateAPIView):
    queryset = Usuario.objects.all()
    serializer_class = CadastroUsuarioSerializers
    permission_classes = [AllowAny]

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