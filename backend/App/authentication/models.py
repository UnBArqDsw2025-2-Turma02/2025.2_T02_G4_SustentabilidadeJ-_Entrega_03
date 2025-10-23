from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """
    Modelo de Usuário do sistema SustentabilidadeJá.
    Extende o modelo padrão do Django para incluir campos específicos.
    """

    # Campos adicionais ao User padrão do Django
    school = models.CharField(
        max_length=200,
        verbose_name="Escola",
        help_text="Nome da escola do usuário",
        blank=True,
        null=True
    )

    grade = models.CharField(
        max_length=50,
        verbose_name="Série/Ano",
        help_text="Série ou ano escolar",
        blank=True,
        null=True
    )

    city = models.CharField(
        max_length=100,
        verbose_name="Cidade",
        help_text="Cidade do usuário",
        blank=True,
        null=True
    )

    total_points = models.IntegerField(
        default=0,
        verbose_name="Total de Pontos",
        help_text="Total de tokens acumulados pelo usuário"
    )

    member_since = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Membro desde",
        help_text="Data de cadastro do usuário"
    )

    class Meta:
        db_table = 'users'
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'
        ordering = ['-date_joined']

    def __str__(self):
        return f"{self.obter_nome_completo() or self.username} - {self.total_points} pontos"

    def obter_nome_completo(self):
        """Retorna o nome completo do usuário."""
        return f"{self.first_name} {self.last_name}".strip() or self.username

    def get_full_name(self):
        """Retorna o nome completo do usuário (compatibilidade Django)."""
        return self.obter_nome_completo()

    def adicionar_pontos(self, quantidade):
        """Adiciona pontos ao total do usuário."""
        self.total_points += quantidade
        self.save()
        return self.total_points

    def remover_pontos(self, quantidade):
        """Remove pontos do total do usuário (para trocas de recompensas)."""
        if self.total_points >= quantidade:
            self.total_points -= quantidade
            self.save()
            return True
        return False

    def obter_saldo_tokens(self):
        """Retorna o saldo atual de tokens do usuário."""
        return self.total_points

    def tem_pontos_suficientes(self, quantidade_necessaria):
        """Verifica se o usuário tem pontos suficientes."""
        return self.total_points >= quantidade_necessaria


# Mantém a classe Usuario original para compatibilidade com os testes
class Usuario:
    """Classe legada para compatibilidade com testes."""

    def __init__(self, nome):
        self.nome = nome
        self.saldoTokens = 0

    def save(self):
        print(f"Usuário {self.nome} com saldo {self.saldoTokens} salvo!")
