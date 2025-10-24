class AcessoNegadoException(PermissionError):
    """Exceção personalizada para acesso negado."""
    def __init__(self, mensagem: str):
        super().__init__(mensagem)