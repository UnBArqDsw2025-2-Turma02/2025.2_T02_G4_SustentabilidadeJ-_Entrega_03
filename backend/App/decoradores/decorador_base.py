class AcaoDecorator:
    """Classe base para decoradores de ações sustentáveis."""

    def __init__(self, componente):
        """Inicializa decorator com componente a ser decorado."""
        self._componente = componente

    def registrar_acao(self, usuario, acao):
        """Delega registro para o componente interno."""
        return self._componente.registrar_acao(usuario, acao)
