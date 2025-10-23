from .decorador_base import AcaoDecorator


class BonusDecorator(AcaoDecorator):
    """Decorator que adiciona bônus de 5 tokens para ações com 20+ tokens."""

    def registrar_acao(self, usuario, acao):
        """Registra ação e adiciona bônus se aplicável."""
        tokens = super().registrar_acao(usuario, acao)

        if tokens >= 20:
            usuario.saldoTokens += 5
            print(f"[BONUS] {usuario.nome} ganhou 5 tokens extras!")

        return tokens
