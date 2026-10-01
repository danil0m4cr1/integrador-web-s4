from django.db import models
from django.contrib.auth.models import User

class Categoria(models.Model):
    nome = models.CharField(max_length = 50)
    descricao = models.CharField(max_length = 100)

    def __str__(self):
        return self.nome

class Laboratorio(models.Model):
    nome = models.CharField(max_length = 50)
    localizacao = models.CharField(max_length = 50)


    def __str__(self):
        return self.nome

class Ativo(models.Model):
    STATUS_CHOICE = [
        ("INDISPONIVEL", "Indisponivel"),
        ("DISPONIVEL", "Disponivel"),
        ("MANUTENCAO", "Manutencao"),
    ]

    patrimonio = models.CharField(max_length = 50)
    nome = models.CharField(max_length = 50)
    descricao = models.CharField(max_length = 100)
    status = models.CharField(
        max_length = 20,
        choices = STATUS_CHOICE,
        default = "INDISPONIVEL",
    )

    laboratorio = models.ForeignKey(
        Laboratorio,
        on_delete = models.SET_NULL,
        null = True,
        blank = True,
        related_name = "ativoslab",
    )

    categoria = models.ForeignKey(
        Categoria,
        on_delete = models.SET_NULL,
        null = True,
        blank = True,
        related_name = "ativoscategoria",
    )

    def __str__(self):
        return f"{self.nome} - (patrimonio={self.patrimonio}) - (laboratorio={self.laboratorio})"

class Usuario(models.Model):
    usuario = models.OneToOneField(
        User, on_delete = models.CASCADE, null = True, blank = True
    )
    nome = models.CharField(max_length = 50)
    email = models.EmailField(unique = True)
    telefone = models.CharField(
        max_length = 50, 
        blank = True
    )

    def __str__(self):
        return self.nome
    
class Movimentacao(models.Model):
    ativo = models.ForeignKey(
        Ativo,
        on_delete = models.SET_NULL,
        null = True,
        blank = True,
        related_name = "movimentacao"
    )
    usuario = models.ForeignKey(
        Usuario,
        on_delete = models.SET_NULL,
        null = True,
        blank = True,
        related_name = "movimentacoes"
    )
    laboratorio_origem = models.CharField(max_length = 50)
    laboratorio_destino = models.CharField(max_length = 50)
    data_movimentacao = models.DateTimeField(auto_now_add = True)
    observacao = models.CharField(max_length = 100)

    def __str__(self):
        return f"Laboratorio origem: {self.laboratorio_origem} - Laboratorio destino: {self.laboratorio_destino}"

    
class OrdemServico(models.Model):
    STATUS_CHOICE = [
        ("CONCLUIDO", "Concluido"),
        ("PENDENTE", "Pendente"),
        ("CANCELADO", "Cancelado")
    ]
    ativo = models.ForeignKey(
        Ativo,
        on_delete = models.SET_NULL,
        null = True,
        blank = True,
        related_name = "ativo"
    )
    usuario = models.ForeignKey(
        Usuario,
        on_delete = models.SET_NULL,
        null = True,
        blank = True,
        related_name = "ordem_servico"
    )
    descricao = models.CharField(max_length = 100)
    status = models.CharField(
        max_length = 20,
        choices = STATUS_CHOICE,
        default = "PENDENTE"
    )
    data_abertura = models.DateTimeField(auto_now_add = True)
    data_fechamento = models.DateTimeField()

    def __str__(self):
        return self.status
