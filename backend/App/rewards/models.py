from django.db import models
from django.conf import settings


class Reward(models.Model):
    """
    Recompensas disponíveis no sistema que podem ser trocadas por tokens.
    """

    TYPE_BADGE = 'Medalha'
    TYPE_DISCOUNT = 'Desconto'
    TYPE_PRIZE = 'Prêmio'
    TYPE_BENEFIT = 'Benefício'

    TYPE_CHOICES = [
        (TYPE_BADGE, 'Medalha/Conquista'),
        (TYPE_DISCOUNT, 'Desconto'),
        (TYPE_PRIZE, 'Prêmio'),
        (TYPE_BENEFIT, 'Benefício'),
    ]

    name = models.CharField(
        max_length=100,
        verbose_name="Nome da Recompensa"
    )

    description = models.TextField(
        verbose_name="Descrição",
        help_text="Descrição detalhada da recompensa"
    )

    required_points = models.IntegerField(
        verbose_name="Pontos Necessários",
        help_text="Quantidade de tokens necessários para desbloquear"
    )

    type = models.CharField(
        max_length=20,
        choices=TYPE_CHOICES,
        verbose_name="Tipo de Recompensa"
    )

    icon = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name="Ícone",
        help_text="Nome do ícone ou emoji"
    )

    image = models.ImageField(
        upload_to='rewards/',
        blank=True,
        null=True,
        verbose_name="Imagem"
    )

    is_active = models.BooleanField(
        default=True,
        verbose_name="Ativa",
        help_text="Se a recompensa está disponível para resgate"
    )

    stock = models.IntegerField(
        default=-1,
        verbose_name="Estoque",
        help_text="Quantidade disponível (-1 para ilimitado)"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'rewards'
        verbose_name = 'Recompensa'
        verbose_name_plural = 'Recompensas'
        ordering = ['required_points', 'name']

    def __str__(self):
        return f"{self.name} ({self.required_points} pontos)"

    def esta_disponivel(self):
        """Verifica se a recompensa está disponível."""
        if not self.is_active:
            return False
        if self.stock == -1:
            return True
        return self.stock > 0

    def is_available(self):
        """Verifica se a recompensa está disponível (compatibilidade)."""
        return self.esta_disponivel()

    def possui_estoque(self):
        """Verifica se há estoque disponível."""
        return self.stock == -1 or self.stock > 0

    def decrementar_estoque(self):
        """Decrementa o estoque da recompensa."""
        if self.stock > 0:
            self.stock -= 1
            self.save()
            return True
        return False

    def pode_ser_resgatada_por(self, usuario):
        """Verifica se a recompensa pode ser resgatada pelo usuário."""
        return (
            self.esta_disponivel() and
            usuario.tem_pontos_suficientes(self.required_points)
        )


class UserReward(models.Model):
    """
    Registro de recompensas resgatadas pelos usuários.
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='user_rewards',
        verbose_name="Usuário"
    )

    reward = models.ForeignKey(
        Reward,
        on_delete=models.PROTECT,
        related_name='user_redemptions',
        verbose_name="Recompensa"
    )

    redeemed_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Data de Resgate"
    )

    points_spent = models.IntegerField(
        verbose_name="Pontos Gastos",
        help_text="Quantidade de pontos gastos no resgate"
    )

    status = models.CharField(
        max_length=20,
        choices=[
            ('Pendente', 'Pendente'),
            ('Entregue', 'Entregue'),
            ('Cancelado', 'Cancelado'),
        ],
        default='Pendente',
        verbose_name="Status"
    )

    notes = models.TextField(
        blank=True,
        verbose_name="Observações"
    )

    class Meta:
        db_table = 'user_rewards'
        verbose_name = 'Resgate de Recompensa'
        verbose_name_plural = 'Resgates de Recompensas'
        ordering = ['-redeemed_at']

    def __str__(self):
        return f"{self.user.username} - {self.reward.name}"

    def esta_pendente(self):
        """Verifica se o resgate está pendente."""
        return self.status == 'Pendente'

    def esta_entregue(self):
        """Verifica se o resgate foi entregue."""
        return self.status == 'Entregue'

    def marcar_como_entregue(self):
        """Marca o resgate como entregue."""
        self.status = 'Entregue'
        self.save()

    def cancelar(self, motivo=""):
        """Cancela o resgate e devolve os pontos ao usuário."""
        if self.status != 'Cancelado':
            self.status = 'Cancelado'
            self.notes = f"Cancelado. {motivo}".strip()
            # Devolve os pontos ao usuário
            self.user.adicionar_pontos(self.points_spent)
            self.save()


class Goal(models.Model):
    """
    Metas de sustentabilidade (globais ou por usuário).
    """

    METRIC_WATER_SAVE = 'water_save'
    METRIC_ENERGY_SAVE = 'energy_save'
    METRIC_ACTION_COUNT = 'action_count'
    METRIC_POINTS = 'points'

    METRIC_CHOICES = [
        (METRIC_WATER_SAVE, 'Economia de Água (litros)'),
        (METRIC_ENERGY_SAVE, 'Economia de Energia (kWh)'),
        (METRIC_ACTION_COUNT, 'Quantidade de Ações'),
        (METRIC_POINTS, 'Pontos Acumulados'),
    ]

    PERIOD_DAILY = 'daily'
    PERIOD_WEEKLY = 'weekly'
    PERIOD_MONTHLY = 'monthly'
    PERIOD_YEARLY = 'yearly'

    PERIOD_CHOICES = [
        (PERIOD_DAILY, 'Diário'),
        (PERIOD_WEEKLY, 'Semanal'),
        (PERIOD_MONTHLY, 'Mensal'),
        (PERIOD_YEARLY, 'Anual'),
    ]

    name = models.CharField(
        max_length=100,
        verbose_name="Nome da Meta"
    )

    description = models.TextField(
        blank=True,
        verbose_name="Descrição"
    )

    target_value = models.IntegerField(
        verbose_name="Valor Alvo",
        help_text="Valor a ser atingido"
    )

    metric = models.CharField(
        max_length=30,
        choices=METRIC_CHOICES,
        verbose_name="Métrica"
    )

    period = models.CharField(
        max_length=20,
        choices=PERIOD_CHOICES,
        verbose_name="Período"
    )

    is_global = models.BooleanField(
        default=True,
        verbose_name="Meta Global",
        help_text="Se True, é uma meta para todos os usuários. Se False, é individual."
    )

    start_date = models.DateField(
        null=True,
        blank=True,
        verbose_name="Data de Início"
    )

    end_date = models.DateField(
        null=True,
        blank=True,
        verbose_name="Data de Término"
    )

    reward = models.ForeignKey(
        Reward,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Recompensa",
        help_text="Recompensa ao atingir a meta"
    )

    is_active = models.BooleanField(
        default=True,
        verbose_name="Ativa"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'goals'
        verbose_name = 'Meta'
        verbose_name_plural = 'Metas'
        ordering = ['-created_at']

    def __str__(self):
        global_str = "Global" if self.is_global else "Individual"
        return f"{self.name} ({global_str}) - {self.target_value} {self.get_metric_display()}"


class UserGoalProgress(models.Model):
    """
    Progresso dos usuários nas metas.
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='goal_progress',
        verbose_name="Usuário"
    )

    goal = models.ForeignKey(
        Goal,
        on_delete=models.CASCADE,
        related_name='user_progress',
        verbose_name="Meta"
    )

    current_value = models.IntegerField(
        default=0,
        verbose_name="Valor Atual",
        help_text="Progresso atual do usuário nesta meta"
    )

    completed = models.BooleanField(
        default=False,
        verbose_name="Completada"
    )

    completed_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Data de Conclusão"
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Última Atualização"
    )

    class Meta:
        db_table = 'user_goal_progress'
        verbose_name = 'Progresso de Meta'
        verbose_name_plural = 'Progressos de Metas'
        unique_together = ['user', 'goal']
        ordering = ['-updated_at']

    def __str__(self):
        return f"{self.user.username} - {self.goal.name}: {self.current_value}/{self.goal.target_value}"

    def porcentagem_progresso(self):
        """Calcula a porcentagem de progresso."""
        if self.goal.target_value == 0:
            return 0
        return min(100, (self.current_value / self.goal.target_value) * 100)

    def progress_percentage(self):
        """Calcula a porcentagem de progresso (compatibilidade)."""
        return self.porcentagem_progresso()

    def esta_completa(self):
        """Verifica se a meta foi completada."""
        return self.completed

    def falta_para_completar(self):
        """Retorna quanto falta para completar a meta."""
        return max(0, self.goal.target_value - self.current_value)

    def atualizar_progresso(self, valor_adicional):
        """Atualiza o progresso da meta."""
        from django.utils import timezone
        self.current_value += valor_adicional

        # Verifica se completou a meta
        if self.current_value >= self.goal.target_value and not self.completed:
            self.completed = True
            self.completed_at = timezone.now()

        self.save()
