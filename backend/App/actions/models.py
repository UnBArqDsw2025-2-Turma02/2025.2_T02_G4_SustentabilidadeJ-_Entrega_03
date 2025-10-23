from django.db import models
from django.conf import settings


class ActionType(models.Model):
    """
    Tipos de ações sustentáveis disponíveis no sistema.
    Exemplos: Reciclagem, Transporte, Economia de Recursos, etc.
    """

    RECICLAGEM = 'Reciclagem'
    TRANSPORTE = 'Transporte'
    ECONOMIA_RECURSOS = 'EconomiaRecursos'
    DESCARTE_CORRETO = 'DescarteCorreto'
    PLANTIO_ARVORE = 'PlantioArvore'

    TYPE_CHOICES = [
        (RECICLAGEM, 'Reciclagem'),
        (TRANSPORTE, 'Transporte Sustentável'),
        (ECONOMIA_RECURSOS, 'Economia de Recursos'),
        (DESCARTE_CORRETO, 'Descarte Correto'),
        (PLANTIO_ARVORE, 'Plantio de Árvore'),
    ]

    name = models.CharField(
        max_length=50,
        unique=True,
        choices=TYPE_CHOICES,
        verbose_name="Nome da Ação",
        help_text="Tipo de ação sustentável"
    )

    description = models.TextField(
        verbose_name="Descrição",
        help_text="Descrição detalhada da ação",
        blank=True
    )

    base_points = models.IntegerField(
        default=10,
        verbose_name="Pontos Base",
        help_text="Quantidade de pontos que esta ação gera"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'action_types'
        verbose_name = 'Tipo de Ação'
        verbose_name_plural = 'Tipos de Ações'
        ordering = ['name']

    def __str__(self):
        return f"{self.get_name_display()} ({self.base_points} pontos)"

    def obter_nome_legivel(self):
        """Retorna o nome da ação em formato legível."""
        return self.get_name_display()


class UserAction(models.Model):
    """
    Registro de ações sustentáveis realizadas pelos usuários.
    """

    STATUS_PENDENTE = 'Pendente'
    STATUS_APROVADA = 'Aprovada'
    STATUS_REJEITADA = 'Rejeitada'

    STATUS_CHOICES = [
        (STATUS_PENDENTE, 'Pendente'),
        (STATUS_APROVADA, 'Aprovada'),
        (STATUS_REJEITADA, 'Rejeitada'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='actions',
        verbose_name="Usuário"
    )

    action_type = models.ForeignKey(
        ActionType,
        on_delete=models.PROTECT,
        related_name='user_actions',
        verbose_name="Tipo de Ação"
    )

    description = models.TextField(
        verbose_name="Descrição",
        help_text="Descrição detalhada da ação realizada",
        blank=True
    )

    proof_url = models.URLField(
        max_length=500,
        verbose_name="URL da Comprovação",
        help_text="Link para foto/vídeo de comprovação",
        blank=True,
        null=True
    )

    proof_file = models.FileField(
        upload_to='actions/proofs/%Y/%m/%d/',
        verbose_name="Arquivo de Comprovação",
        help_text="Upload de foto/vídeo de comprovação",
        blank=True,
        null=True
    )

    location = models.CharField(
        max_length=200,
        verbose_name="Localização",
        help_text="Local onde a ação foi realizada",
        blank=True,
        null=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_PENDENTE,
        verbose_name="Status"
    )

    points_awarded = models.IntegerField(
        default=0,
        verbose_name="Pontos Concedidos",
        help_text="Quantidade de pontos atribuídos por esta ação"
    )

    date = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Data de Registro"
    )

    approved_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Data de Aprovação"
    )

    approved_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='approved_actions',
        verbose_name="Aprovado por"
    )

    class Meta:
        db_table = 'user_actions'
        verbose_name = 'Ação do Usuário'
        verbose_name_plural = 'Ações dos Usuários'
        ordering = ['-date']

    def __str__(self):
        return f"{self.user.username} - {self.action_type.name} ({self.status})"

    def esta_aprovada(self):
        """Verifica se a ação foi aprovada."""
        return self.status == self.STATUS_APROVADA

    def esta_pendente(self):
        """Verifica se a ação está pendente de aprovação."""
        return self.status == self.STATUS_PENDENTE

    def aprovar(self, aprovador):
        """Aprova a ação e atribui os pontos."""
        from django.utils import timezone
        self.status = self.STATUS_APROVADA
        self.approved_by = aprovador
        self.approved_at = timezone.now()
        self.points_awarded = self.action_type.base_points
        self.save()

    def rejeitar(self, aprovador):
        """Rejeita a ação."""
        from django.utils import timezone
        self.status = self.STATUS_REJEITADA
        self.approved_by = aprovador
        self.approved_at = timezone.now()
        self.save()


class BillRecord(models.Model):
    """
    Registro de contas de água e energia para cálculo de economia.
    """

    BILL_TYPE_WATER = 'Água'
    BILL_TYPE_ENERGY = 'Energia'

    BILL_TYPE_CHOICES = [
        (BILL_TYPE_WATER, 'Água'),
        (BILL_TYPE_ENERGY, 'Energia'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='bills',
        verbose_name="Usuário"
    )

    type = models.CharField(
        max_length=20,
        choices=BILL_TYPE_CHOICES,
        verbose_name="Tipo de Conta"
    )

    consumption_value = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Valor de Consumo",
        help_text="Consumo em m³ (água) ou kWh (energia)"
    )

    value_rs = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Valor em R$",
        help_text="Valor da conta em reais"
    )

    photo_url = models.URLField(
        max_length=500,
        verbose_name="URL da Foto",
        blank=True,
        null=True
    )

    photo_file = models.ImageField(
        upload_to='bills/%Y/%m/',
        verbose_name="Foto da Conta",
        help_text="Upload da foto da conta",
        blank=True,
        null=True
    )

    month = models.IntegerField(
        verbose_name="Mês",
        help_text="Mês de referência (1-12)"
    )

    year = models.IntegerField(
        verbose_name="Ano",
        help_text="Ano de referência"
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Data de Registro"
    )

    class Meta:
        db_table = 'bill_records'
        verbose_name = 'Registro de Conta'
        verbose_name_plural = 'Registros de Contas'
        ordering = ['-year', '-month']
        unique_together = ['user', 'type', 'month', 'year']

    def __str__(self):
        return f"{self.user.username} - {self.type} {self.month}/{self.year}"

    def obter_periodo(self):
        """Retorna o período da conta em formato legível."""
        return f"{self.month:02d}/{self.year}"

    def calcular_economia(self):
        """Calcula a economia em relação ao mês anterior."""
        # Busca a conta do mês anterior
        mes_anterior = self.month - 1 if self.month > 1 else 12
        ano_anterior = self.year if self.month > 1 else self.year - 1

        try:
            conta_anterior = BillRecord.objects.get(
                user=self.user,
                type=self.type,
                month=mes_anterior,
                year=ano_anterior
            )
            economia = conta_anterior.consumption_value - self.consumption_value
            return max(0, economia)  # Retorna 0 se não houve economia
        except BillRecord.DoesNotExist:
            return 0


# Mantém a classe AcaoSustentavel original para compatibilidade com testes
class AcaoSustentavel:
    """Classe legada para compatibilidade com testes."""

    def __init__(self, tipoAcao):
        self.tipoAcao = tipoAcao
        self.validada = False

    def save(self):
        print(f"Ação '{self.tipoAcao}' salva com sucesso!")
