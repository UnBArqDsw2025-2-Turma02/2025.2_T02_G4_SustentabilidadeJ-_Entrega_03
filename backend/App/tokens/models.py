from django.db import models
from django.conf import settings


class TokenLedger(models.Model):
    """
    Ledger (livro razão) de tokens - registra todas as transações de tokens.
    Cada entrada representa um crédito ou débito de tokens.
    """

    TYPE_CREDIT = 'Crédito'
    TYPE_DEBIT = 'Débito'

    TYPE_CHOICES = [
        (TYPE_CREDIT, 'Crédito'),
        (TYPE_DEBIT, 'Débito'),
    ]

    SOURCE_ACTION = 'Ação'
    SOURCE_REWARD = 'Troca'
    SOURCE_BONUS = 'Bônus'
    SOURCE_ADMIN = 'Administrativo'

    SOURCE_CHOICES = [
        (SOURCE_ACTION, 'Ação Sustentável'),
        (SOURCE_REWARD, 'Troca por Recompensa'),
        (SOURCE_BONUS, 'Bônus'),
        (SOURCE_ADMIN, 'Ajuste Administrativo'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='token_transactions',
        verbose_name="Usuário"
    )

    amount = models.IntegerField(
        verbose_name="Quantidade",
        help_text="Quantidade de tokens (positivo para crédito, negativo para débito)"
    )

    type = models.CharField(
        max_length=20,
        choices=TYPE_CHOICES,
        verbose_name="Tipo de Transação"
    )

    source = models.CharField(
        max_length=30,
        choices=SOURCE_CHOICES,
        verbose_name="Origem",
        help_text="Origem dos tokens"
    )

    reference_id = models.IntegerField(
        null=True,
        blank=True,
        verbose_name="ID de Referência",
        help_text="ID da ação ou recompensa relacionada"
    )

    description = models.TextField(
        blank=True,
        verbose_name="Descrição",
        help_text="Descrição da transação"
    )

    date = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Data da Transação"
    )

    balance_after = models.IntegerField(
        default=0,
        verbose_name="Saldo Após",
        help_text="Saldo do usuário após esta transação"
    )

    class Meta:
        db_table = 'token_ledger'
        verbose_name = 'Transação de Token'
        verbose_name_plural = 'Transações de Tokens'
        ordering = ['-date']
        indexes = [
            models.Index(fields=['user', '-date']),
            models.Index(fields=['type', '-date']),
        ]

    def __str__(self):
        return f"{self.user.username} - {self.type} {self.amount} tokens ({self.source})"

    def save(self, *args, **kwargs):
        """Atualiza o saldo do usuário ao salvar a transação."""
        if not self.pk:  # Apenas em criação
            # Atualiza o total_points do usuário
            if self.type == self.TYPE_CREDIT:
                self.user.total_points += self.amount
            else:
                self.user.total_points -= self.amount

            self.balance_after = self.user.total_points
            self.user.save()

        super().save(*args, **kwargs)

    def eh_credito(self):
        """Verifica se a transação é um crédito."""
        return self.type == self.TYPE_CREDIT

    def eh_debito(self):
        """Verifica se a transação é um débito."""
        return self.type == self.TYPE_DEBIT

    def obter_descricao_completa(self):
        """Retorna uma descrição completa da transação."""
        tipo_texto = "Ganhou" if self.eh_credito() else "Gastou"
        return f"{tipo_texto} {abs(self.amount)} tokens - {self.get_source_display()}"


# Mantém a classe Token original para compatibilidade com testes
class Token:
    """Classe legada para compatibilidade com testes."""

    def __init__(self, quantidade=0):
        self.quantidade = quantidade
