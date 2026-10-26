from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse
from rest_framework.routers import DefaultRouter
from ativos.views import (
    home, 
    AtivoViewSet, 
    CategoriaViewSet, 
    CadastroUsuarioViewSet, 
    LaboratorioViewSet, 
    MovimentacaoViewSet, 
    OrdemServicoViewSet,
    UsuarioViewSet,
    login_usuario
)

def home(request):
    return HttpResponse("Django Teste - Projeto Integrador")

router = DefaultRouter()

router.register(r'ativo', AtivoViewSet, basename = 'ativo')
router.register(r'categoria', CategoriaViewSet, basename = 'categoria')
router.register(r'laboratorio', LaboratorioViewSet, basename = 'laboratorio')
router.register(r'movimentacao', MovimentacaoViewSet, basename = 'movimentacao')
router.register(r'ordem-servico', OrdemServicoViewSet, basename = 'ordem-servico')
router.register(r'usuario', UsuarioViewSet, basename = 'usuario')

urlpatterns = [
    path('', home),
    path('admin/', admin.site.urls),
    path('api/usuarios/cadastrar/', CadastroUsuarioViewSet.as_view(), name = 'cadastrar_usuario'),
    path('api/usuarios/login/', login_usuario, name = 'login_usuario'),
    path('api/', include(router.urls)),
]
