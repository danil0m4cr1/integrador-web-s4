"""
URL configuration for lab project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse
from rest_framework.routers import DefaultRouter
from produtos.views import (
    home, 
    AtivoViewSet, 
    CategoriaViewSet, 
    CadastroUsuarioViewSet, 
    LaboratorioViewSet, 
    MovimentacaoViewSet, 
    OrdemServicoViewSet
)

def home(request):
    return HttpResponse("Django Teste - Projeto Integrador")

router = DefaultRouter()
router.register(r'ativo', AtivoViewSet, basename = 'ativo')
router.register(r'categoria', CategoriaViewSet, basename = 'categoria')
router.register(r'laboratorio', LaboratorioViewSet, basename = 'laboratorio')
router.register(r'movimentacao', MovimentacaoViewSet, basename = 'movimentacao')
router.register(r'ordem-servico', OrdemServicoViewSet, basename = 'ordem-servico')

urlpatterns = [
    path('', home),
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/usuarios/cadastrar/', CadastroUsuarioViewSet.as_view(), name = 'cadastrar_usuario')
]
