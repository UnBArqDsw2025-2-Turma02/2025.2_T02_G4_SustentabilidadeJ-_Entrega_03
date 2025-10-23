from .base_decorator import AcaoDecorator

class BonusDecorator(AcaoDecorator):
    def registrar_acao(self, usuario, acao):
        tokens = super().registrar_acao(usuario, acao)
        if tokens >= 20:
            usuario.saldoTokens += 5
            print(f"[BÔNUS] {usuario.nome} ganhou 5 tokens extras!")
        return tokens

