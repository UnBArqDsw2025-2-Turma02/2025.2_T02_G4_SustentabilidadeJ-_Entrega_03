from .base_decorator import AcaoDecorator

class LogDecorator(AcaoDecorator):
    def registrar_acao(self, usuario, acao):
        print(f"[LOG] Registrando ação '{acao.tipoAcao}' de {usuario.nome}")
        return super().registrar_acao(usuario, acao)
