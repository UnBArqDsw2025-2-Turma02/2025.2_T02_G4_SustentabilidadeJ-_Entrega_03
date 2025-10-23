from .decorador_base import AcaoDecorator

# Padrão de Projeto Estrutural: Decorator
# Este decorator adiciona um "diário" do que acontece no sistema!

class LogDecorator(AcaoDecorator):
    """
    Decorator de Log - O Repórter do Sistema!

    Este decorator é como um repórter que anota tudo que acontece.
    Toda vez que alguém registra uma ação, ele imprime uma mensagem
    dizendo quem fez o quê.

    Por que isso é útil?
    📝 Auditoria: Você consegue ver tudo que aconteceu no sistema
    🐛 Debug: Ajuda a encontrar problemas durante o desenvolvimento
    👀 Monitoramento: Acompanhe as atividades dos usuários em tempo real

    Exemplo de uso:
        servico = RegistraAcaoService(token_service)
        servico_com_log = LogDecorator(servico)

        # Agora toda ação vai aparecer no log!
        servico_com_log.registrar_acao(joao, acao)
        # Vai imprimir: [LOG] Registrando ação 'Reciclagem' de João
    """

    def registrar_acao(self, usuario, acao):
        """
        Registra a ação E imprime uma mensagem de log.

        Funciona assim:
        1. ANTES: Imprime quem está fazendo o quê
        2. DURANTE: Chama o próximo componente (pode ser outro decorator ou o serviço)
        3. DEPOIS: Retorna os tokens que foram dados

        A mensagem de log mostra:
        [LOG] Registrando ação 'NomeDaAção' de NomeDoUsuário

        Parâmetros:
            usuario: A pessoa fazendo a ação
            acao: A ação sustentável sendo registrada

        Retorna:
            Quantos tokens foram dados (vem do próximo componente na cadeia)

        Exemplo:
            >>> log_decorator.registrar_acao(maria, acao_plantar)
            [LOG] Registrando ação 'PlantioArvore' de Maria
            25
        """
        # Imprime o log ANTES de processar
        print(f"[LOG] Registrando ação '{acao.tipoAcao}' de {usuario.nome}")

        # Passa para o próximo componente fazer o trabalho
        return super().registrar_acao(usuario, acao)
