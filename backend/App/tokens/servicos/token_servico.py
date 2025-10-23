    from strategies import (
        ReciclagemStrategy, TransporteStrategy,
        EconomiaRecursosStrategy, DescarteCorretoStrategy,
        PlantioArvoreStrategy
    )

    #possui singleton
    class TokenService:
        _instance = None  #atributo de classe que guardará a instância única

        def __new__(cls):
            #cria uma instancia se ainda não existir.
            if cls._instance is None:
                cls._instance = super(TokenService, cls).__new__(cls)
            return cls._instance

        def __init__(self):
            if not hasattr(self, "strategies"):
                self.strategies = {
                    "Reciclagem": ReciclagemStrategy(),
                    "Transporte": TransporteStrategy(),
                    "EconomiaRecursos": EconomiaRecursosStrategy(),
                    "DescarteCorreto": DescarteCorretoStrategy(),
                    "PlantioArvore": PlantioArvoreStrategy()
                }

        def registrar_tokens(self, usuario, acao):
            strategy = self.strategies.get(acao.tipoAcao)
            if not strategy:
                return 0  # caso ação não tenha estratégia definida
            tokens = strategy.calcular_tokens(acao)
            usuario.saldoTokens += tokens
            #aqui persistiria no banco (ex: usuario.save())
            return tokens
