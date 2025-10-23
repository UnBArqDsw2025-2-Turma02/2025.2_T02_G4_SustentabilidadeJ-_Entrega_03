from .decorador_base import AcaoDecorator

# Padrão de Projeto Estrutural: Decorator
# Este decorator é tipo um "prêmio surpresa" para ações incríveis!

class BonusDecorator(AcaoDecorator):
    """
    Decorator de Bônus - O Sistema de Recompensas Extras!

    Sabe quando você faz algo muito legal e ganha um presentinho extra?
    É isso que este decorator faz! Quando alguém faz uma ação de grande
    impacto (que dá 20+ tokens), ganha 5 tokens de bônus!

    🎁 Como funciona o bônus:
    - Ação pequena (menos de 20 tokens): sem bônus, mas já é ótimo!
    - Ação grande (20 ou mais tokens): BOOM! +5 tokens de bônus! 🎉

    📊 Exemplos práticos:
    - Reciclagem (10 tokens): total = 10 tokens (sem bônus)
    - Transporte (15 tokens): total = 15 tokens (sem bônus)
    - Economia de Recursos (20 tokens): total = 25 tokens (20 + 5 de bônus!)
    - Plantio de Árvore (25 tokens): total = 30 tokens (25 + 5 de bônus!)

    💡 Objetivo: Incentivar ações de maior impacto ambiental!
    """

    def registrar_acao(self, usuario, acao):
        """
        Registra a ação e dá um bônus surpresa para ações incríveis!

        Sequência de eventos:
        1. PRIMEIRO: Chama o próximo componente para processar tudo
        2. SEGUNDO: Recebe quantos tokens foram dados
        3. TERCEIRO: Se foram 20+ tokens, dá bônus de 5 tokens!
        4. QUARTO: Avisa o usuário que ele ganhou bônus (se ganhou)
        5. QUINTO: Retorna os tokens originais

        Parâmetros:
            usuario: A pessoa incrível fazendo a ação
            acao: A ação sustentável que foi feita

        Retorna:
            Tokens originais da ação (o bônus é adicionado direto no saldo)

        Exemplo:
            >>> bonus_decorator.registrar_acao(ana, acao_plantar_arvore)
            [BONUS] Ana ganhou 5 tokens extras!
            25  # Retorna 25, mas Ana tem 30 no saldo (25 + 5 bônus)
        """
        # Primeiro deixa os outros componentes trabalharem
        tokens = super().registrar_acao(usuario, acao)

        # Agora vamos ver se merece bônus! 🎁
        if tokens >= 20:
            # SIM! Adiciona 5 tokens de bônus
            usuario.saldoTokens += 5

            # Avisa que ganhou bônus (todo mundo gosta de ser parabenizado!)
            print(f"[BONUS] {usuario.nome} ganhou 5 tokens extras! 🌟")

        return tokens
