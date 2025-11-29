# page_app/models.py
from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError


class UsuarioSistema(models.Model):
    """
    Usuários que acessam o sistema (técnico, administrador etc.).
    Não é o User padrão do Django, é um modelo simples para o trabalho.
    """
    nome = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=50, unique=True)
    senha = models.CharField(max_length=128)  # simples (sem hash) para fins acadêmicos
    ativo = models.BooleanField(default=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome


class Colaborador(models.Model):
    nome = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    telefone = models.CharField(max_length=20, blank=True)
    ativo = models.BooleanField(default=True)

    def __str__(self):
        return self.nome


class Equipamento(models.Model):
    nome = models.CharField(max_length=150)
    descricao = models.TextField(blank=True)
    codigo = models.CharField(max_length=50, unique=True, verbose_name="Código/Patrimônio")
    ca = models.CharField(max_length=30, blank=True, verbose_name="Certificado de Aprovação (CA)")
    quantidade_estoque = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.nome


class ControleEPI(models.Model):
    STATUS_CHOICES = [
        ('EMPRESTADO', 'Emprestado'),
        ('EM_USO', 'Em uso'),
        ('FORNECIDO', 'Fornecido'),
        ('DEVOLVIDO', 'Devolvido'),
        ('DANIFICADO', 'Danificado'),
        ('PERDIDO', 'Perdido'),
    ]

    colaborador = models.ForeignKey(
        Colaborador,
        on_delete=models.CASCADE,
        related_name='movimentos'
    )
    equipamento = models.ForeignKey(
        Equipamento,
        on_delete=models.CASCADE,
        related_name='movimentos'
    )

    data_entrega = models.DateTimeField(
        default=timezone.now,
        verbose_name="Data da entrega"
    )
    data_prevista_devolucao = models.DateTimeField(
        verbose_name="Data prevista para devolução"
    )
    data_devolucao = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Data da devolução"
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='EMPRESTADO'
    )
    observacao = models.TextField(
        blank=True,
        verbose_name="Observações gerais"
    )
    observacao_devolucao = models.TextField(
        blank=True,
        verbose_name="Observação na devolução"
    )

    def __str__(self):
        return f"{self.colaborador} - {self.equipamento} ({self.status})"

    def clean(self):
        """
        Regras de negócio:
        - No cadastro, a data prevista de devolução deve ser maior que a data/hora atual.
        - Se o status for DEVOLVIDO, DANIFICADO ou PERDIDO:
            - exigir data_devolucao
            - exigir observacao_devolucao
        """
        errors = {}

        # Só força "futuro" no ato do cadastro (quando não existe pk ainda)
        if not self.pk and self.data_prevista_devolucao <= timezone.now():
            errors["data_prevista_devolucao"] = "A data prevista deve ser maior que a data/hora atual."

        status_finais = ['DEVOLVIDO', 'DANIFICADO', 'PERDIDO']
        if self.status in status_finais:
            if not self.data_devolucao:
                errors["data_devolucao"] = "Informe a data da devolução."
            if not self.observacao_devolucao:
                errors["observacao_devolucao"] = "Informe uma observação da devolução."

        if errors:
            raise ValidationError(errors)
