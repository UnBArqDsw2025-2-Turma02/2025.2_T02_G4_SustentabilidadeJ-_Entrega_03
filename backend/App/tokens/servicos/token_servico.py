from .token_strategy import (
    ReciclagemStrategy, TransporteStrategy,
    EconomiaRecursosStrategy, DescarteCorretoStrategy,
    PlantioArvoreStrategy
)

# Padrão de Projeto Criacional: Singleton
#
# O padrão Singleton garante que só existe UMA instância deste serviço em toda a aplicação.
# Não importa quantas vezes você chame TokenService(), sempre receberá o mesmo objeto.
# Isso é importante para garantir que todas as partes do sistema usem as mesmas estratégias.

class TokenService:
    """
    Serviço Central de Gerenciamento de Tokens.

    Este é o coração do sistema de pontuação! Ele:
    1. Usa o padrão Singleton - só existe uma instância dele no sistema
    2. Usa o padrão Strategy - cada tipo de ação tem seu próprio cálculo
    3. Distribui tokens para os usuários de acordo com suas ações sustentáveis

    Exemplos de uso:
        servico = TokenService()  # Sempre retorna a mesma instância
        tokens = servico.registrar_tokens(usuario, acao)
    """

    # Esta variável guarda a única instância do serviço
    _instance = None

    def __new__(cls):
        """
        Método mágico do Python que controla a criação de objetos.

        Se já existe uma instância, retorna ela.
        Se não existe, cria uma nova e guarda para o futuro.

        É assim que implementamos o padrão Singleton!
        """
        if cls._instance is None:
            cls._instance = super(TokenService, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        """
        Prepara o serviço para funcionar.

        Cria um "cardápio" de estratégias onde cada tipo de ação
        sabe exatamente quantos tokens deve dar.

        Só roda uma vez, mesmo que você tente criar várias "instâncias".
        """
        if not hasattr(self, "estrategias"):
            # Cardápio de estratégias - cada ação tem sua própria regra
            self.estrategias = {
                "Reciclagem": ReciclagemStrategy(),
                "Transporte": TransporteStrategy(),
                "EconomiaRecursos": EconomiaRecursosStrategy(),
                "DescarteCorreto": DescarteCorretoStrategy(),
                "PlantioArvore": PlantioArvoreStrategy()
            }
            # Mantém compatibilidade com código antigo
            self.strategies = self.estrategias

    def registrar_tokens(self, usuario, acao):
        """
        Dá tokens para o usuário que fez uma ação sustentável!

        Como funciona:
        1. Pega o tipo da ação (ex: "Reciclagem")
        2. Encontra a estratégia certa para calcular os tokens
        3. Calcula quantos tokens a pessoa merece
        4. Adiciona no saldo do usuário
        5. Retorna quantos tokens foram dados

        Parâmetros:
            usuario: A pessoa que vai receber os tokens
            acao: A ação sustentável que ela fez

        Retorna:
            Quantos tokens foram dados (número inteiro)

        Exemplo:
            >>> servico = TokenService()
            >>> tokens = servico.registrar_tokens(maria, acao_reciclagem)
            >>> print(f"Você ganhou {tokens} tokens!")
        """
        # Procura a estratégia certa para esta ação
        estrategia = self.estrategias.get(acao.tipoAcao)

        # Se não conhecemos este tipo de ação, não dá tokens
        if not estrategia:
            return 0

        # Usa a estratégia para calcular os tokens
        tokens = estrategia.calcular_tokens(acao)

        # Adiciona os tokens no saldo do usuário
        usuario.saldoTokens += tokens

        # Em produção, aqui salvamos no banco de dados
        # Exemplo: usuario.save()

        return tokens

    def obter_estrategia(self, tipo_acao):
        """
        Retorna a estratégia de cálculo para um tipo de ação.

        Útil quando você quer saber quanto vale uma ação antes de registrá-la.

        Parâmetros:
            tipo_acao: Nome do tipo de ação (ex: "PlantioArvore")

        Retorna:
            A estratégia correspondente ou None se não existir
        """
        return self.estrategias.get(tipo_acao)

    def listar_tipos_disponiveis(self):
        """
        Lista todos os tipos de ações que o sistema conhece.

        Retorna:
            Lista com os nomes dos tipos de ações disponíveis
        """
        return list(self.estrategias.keys())
