# Padrão de Projeto Estrutural: Decorator (Decorador)
#
# O padrão Decorator é como adicionar acessórios a um carro:
# - Você tem o carro base (o serviço de registro)
# - Pode adicionar ar-condicionado (LogDecorator)
# - Pode adicionar som automotivo (BonusDecorator)
# - Pode adicionar os dois juntos!
#
# Cada decorator "envolve" o componente anterior, adicionando sua funcionalidade
# sem modificar o código original. É tipo colocar uma boneca russa dentro da outra!

class AcaoDecorator:
    """
    Classe Base para Decoradores de Ações Sustentáveis.

    Esta é a "forma base" que todos os decoradores seguem.
    Pense nela como um molde que garante que todos os decoradores
    funcionem da mesma maneira e possam ser combinados livremente.

    Como usar:
    1. Crie uma classe que herda desta
    2. Sobrescreva o método registrar_acao()
    3. Adicione sua funcionalidade especial
    4. Chame super().registrar_acao() para passar para o próximo

    Exemplo de combinação:
        servico_base = RegistraAcaoService(token_service)
        com_log = LogDecorator(servico_base)
        com_tudo = BonusDecorator(com_log)

    Agora, quando você usar 'com_tudo', vai ter log E bônus!
    """

    def __init__(self, componente):
        """
        Prepara o decorator para "envolver" outro componente.

        Parâmetros:
            componente: Pode ser:
                       - O serviço original (RegistraAcaoService)
                       - Outro decorator (para fazer uma cadeia)

                       Exemplo de cadeia:
                       BonusDecorator(LogDecorator(servico_base))
                                      ^           ^
                                      |           |
                                   componente  componente do Log
        """
        self._componente = componente

    def registrar_acao(self, usuario, acao):
        """
        Registra uma ação - mas deixa para o componente interno fazer o trabalho.

        Este método é como um "passe adiante" - ele simplesmente chama
        o próximo componente da cadeia. Decoradores concretos vão sobrescrever
        este método para adicionar suas funcionalidades especiais.

        Como funciona na prática:
        1. Decorador pode fazer algo ANTES (ex: imprimir log)
        2. Chama super().registrar_acao() ou self._componente.registrar_acao()
        3. Decorador pode fazer algo DEPOIS (ex: dar bônus)

        Parâmetros:
            usuario: A pessoa que está fazendo a ação sustentável
            acao: A ação que foi feita (reciclagem, plantio, etc)

        Retorna:
            Quantidade de tokens que foram dados ao usuário
        """
        return self._componente.registrar_acao(usuario, acao)
