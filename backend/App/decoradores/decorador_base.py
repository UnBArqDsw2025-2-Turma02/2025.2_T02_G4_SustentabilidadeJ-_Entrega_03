class AcaoDecorator:
    def __init__(self, componente):
        self._componente = componente

    def registrar_acao(self, usuario, acao):
        return self._componente.registrar_acao(usuario, acao)
