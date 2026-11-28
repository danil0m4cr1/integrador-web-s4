from django.db import models
from django.contrib.auth.models import User


class Categoria(models.Model):
    nome = models.CharField(max_length=50)
    descricao = models.CharField(max_length=100)

    def __str__(self):
        return self.nome


class Laboratorio(models.Model):
    nome = models.CharField(max_length=50)
    localizacao = models.CharField(max_length=50)

    def __str__(self):
        return self.nome


class Ativo(models.Model):
    STATUS_CHOICE = [
        ("INDISPONIVEL", "Indisponivel"),
        ("DISPONIVEL", "Disponivel"),
        ("MANUTENCAO", "Manutencao"),
    ]

    patrimonio = models.CharField(max_length=50)
    nome = models.CharField(max_length=50)
    descricao = models.CharField(max_length=100)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICE,
        default="INDISPONIVEL",
    )

    laboratorio = models.ForeignKey(
        Laboratorio,
        on_delete=models.PROTECT,
        related_name="ativoslab",
    )

    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.PROTECT,
        related_name="ativoscategoria",
    )

    def __str__(self):
        return (
            f"{self.nome} - (patrimonio={self.patrimonio}) "
            f"- (laboratorio={self.laboratorio})"
        )


class Movimentacao(models.Model):
    ativo = models.ForeignKey(
        Ativo,
        on_delete=models.PROTECT,
        related_name="movimentacao",
    )

    usuario = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="movimentacoes",
    )

    laboratorio_origem = models.CharField(max_length=50)
    laboratorio_destino = models.CharField(max_length=50)
    data_movimentacao = models.DateTimeField(auto_now_add=True)
    observacao = models.CharField(max_length=100)

    def __str__(self):
        return (
            f"Laboratorio origem: {self.laboratorio_origem} "
            f"- Laboratorio destino: {self.laboratorio_destino}"
        )


class OrdemServico(models.Model):
    STATUS_CHOICE = [
        ("CONCLUIDO", "Concluido"),
        ("PENDENTE", "Pendente"),
        ("CANCELADO", "Cancelado"),
    ]

    ativo = models.ForeignKey(
        Ativo,
        on_delete=models.PROTECT,
        related_name="ordens_servico",
    )

    usuario = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="ordem_servico",
    )

    descricao = models.CharField(max_length=100)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICE,
        default="PENDENTE",
    )

    laboratorio_origem = models.CharField(max_length=50)
    laboratorio_destino = models.CharField(max_length=50)

    data_abertura = models.DateTimeField(auto_now_add=True)

    data_fechamento = models.DateTimeField(
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.status

    def atualizar_status_ativo(self, ativo_id):
        if not ativo_id:
            return

        ativo = Ativo.objects.filter(id=ativo_id).first()

        if not ativo:
            return

        ordens = OrdemServico.objects.filter(ativo_id=ativo_id)

        if ordens.filter(status="PENDENTE").exists():
            novo_status = "MANUTENCAO"

        elif ordens.filter(status="CONCLUIDO").exists():
            novo_status = "DISPONIVEL"

        elif ordens.filter(status="CANCELADO").exists():
            novo_status = "INDISPONIVEL"

        else:
            return

        if ativo.status != novo_status:
            ativo.status = novo_status
            ativo.save(update_fields=["status"])

    def save(self, *args, **kwargs):
        ativo_anterior_id = None

        if self.pk:
            ordem_anterior = (
                OrdemServico.objects
                .filter(pk=self.pk)
                .values("ativo_id")
                .first()
            )

            if ordem_anterior:
                ativo_anterior_id = ordem_anterior["ativo_id"]

        super().save(*args, **kwargs)

        if ativo_anterior_id and ativo_anterior_id != self.ativo_id:
            self.atualizar_status_ativo(ativo_anterior_id)

        self.atualizar_status_ativo(self.ativo_id)

    def delete(self, *args, **kwargs):
        ativo_id = self.ativo_id

        super().delete(*args, **kwargs)

        self.atualizar_status_ativo(ativo_id)
