
from rest_framework import viewsets, generics, status
from rest_framework.permissions import AllowAny
from rest_framework.decorators import (
    api_view,
    permission_classes
)
from rest_framework.response import Response

from django.http import HttpResponse
from django.contrib.auth import authenticate

from rest_framework_simplejwt.tokens import RefreshToken

from .models import (
    Categoria,
    Laboratorio,
    Ativo,
    Movimentacao,
    OrdemServico
)
from django.contrib.auth.models import User

from .serializers import (
    CadastroUsuarioSerializers,
    UsuarioSerializer,
    CategoriaSerializer,
    LaboratorioSerializer,
    AtivoSerializer,
    MovimentacaoSerializer,
    OrdemServicoSerializer
)

from .permissions import SomenteAdminParaAlteracoes


def home(request):
    return HttpResponse("Django Teste - Projeto Integrador")

class CadastroUsuarioViewSet(generics.CreateAPIView):

    queryset = UsuarioModel.objects.all()
    serializer_class = CadastroUsuarioSerializers

    permission_classes = [AllowAny]

class UsuarioViewSet(viewsets.ReadOnlyModelViewSet):

    queryset = UsuarioModel.objects.all().order_by("-id")
    serializer_class = UsuarioSerializer

    
    permission_classes = [SomenteAdminParaAlteracoes]

class CategoriaViewSet(viewsets.ModelViewSet):

    queryset = Categoria.objects.all().order_by("-id")
    serializer_class = CategoriaSerializer

    permission_classes = [SomenteAdminParaAlteracoes]

class LaboratorioViewSet(viewsets.ModelViewSet):

    queryset = Laboratorio.objects.all().order_by("-id")
    serializer_class = LaboratorioSerializer

    permission_classes = [SomenteAdminParaAlteracoes]

class AtivoViewSet(viewsets.ModelViewSet):

    queryset = Ativo.objects.all().order_by("-id")
    serializer_class = AtivoSerializer

    permission_classes = [SomenteAdminParaAlteracoes]

class MovimentacaoViewSet(viewsets.ModelViewSet):

    queryset = Movimentacao.objects.all().order_by("-id")
    serializer_class = MovimentacaoSerializer

    permission_classes = [SomenteAdminParaAlteracoes]

class OrdemServicoViewSet(viewsets.ModelViewSet):

    queryset = OrdemServico.objects.all().order_by("-id")
    serializer_class = OrdemServicoSerializer

    permission_classes = [SomenteAdminParaAlteracoes]



@api_view(['POST'])
@permission_classes([AllowAny])
def login_usuario(request):

    email = request.data.get('email', '').strip().lower()
    password = request.data.get('password', '')

    if not email or not password:
        return Response(
            {'detail': 'Informe o e-mail e a senha.'},
            status=status.HTTP_400_BAD_REQUEST
        )

    usuario_cadastrado = User.objects.filter(
        email__iexact=email
    ).first()

    if usuario_cadastrado is None:
        return Response(
            {'detail': 'E-mail ou senha inválidos.'},
            status=status.HTTP_401_UNAUTHORIZED
        )

    usuario = authenticate(
        request,
        username=usuario_cadastrado.username,
        password=password
    )

    if usuario is None:
        return Response(
            {'detail': 'E-mail ou senha inválidos.'},
            status=status.HTTP_401_UNAUTHORIZED
        )

    if not usuario.is_active:
        return Response(
            {'detail': 'Usuário inativo.'},
            status=status.HTTP_403_FORBIDDEN
        )

    refresh = RefreshToken.for_user(usuario)

    return Response({
        'id': usuario.id,
        'email': usuario.email,
        'is_staff': usuario.is_staff,
        'access': str(refresh.access_token),
        'refresh': str(refresh),
        'detail': 'Login realizado com sucesso.'
    }, status=status.HTTP_200_OK)
