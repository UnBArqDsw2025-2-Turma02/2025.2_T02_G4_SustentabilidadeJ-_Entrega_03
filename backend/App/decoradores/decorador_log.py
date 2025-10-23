from .decorador_base import AcaoDecorator


class LogDecorator(AcaoDecorator):
    """Decorator que adiciona logging ao registro de ações."""

    def registrar_acao(self, usuario, acao):
        """Registra ação com log."""
        print(f"[LOG] Registrando ação '{acao.tipoAcao}' de {usuario.nome}")
        return super().registrar_acao(usuario, acao)
