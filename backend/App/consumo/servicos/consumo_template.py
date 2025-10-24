from abc import ABC, abstractmethod
from typing import Dict, Any

class ConsumoTemplate(ABC):
    """
    Classe Abstrata que define o esqueleto do algoritmo para análise de consumo.
    Implementa o padrão de projeto Template Method.
    """

    def __init__(self, email_usuario: str):
        """Inicializa com o email do usuário."""
        self.email_usuario = email_usuario

    def analisar_consumo(self, dados_usuario: Dict[str, Any]) -> Dict[str, Any]:
        """
        Template Method: Define a sequência de passos para analisar o consumo.
        Os passos concretos são delegados às subclasses.
        """
        # 1. Calcular o consumo específico (passo abstrato)
        consumo_atual = self.calcular_consumo(dados_usuario)

        # 2. Obter a média histórica ou meta (passo abstrato)
        media_historica = self.obter_media()

        # 3. Verificar se o consumo está acima da média/meta (passo abstrato)
        alerta_necessario = self.verificar_alerta(consumo_atual, media_historica)

        # 4. Gerar a mensagem de alerta/feedback (passo concreto)
        mensagem_feedback = self.gerar_alerta(alerta_necessario, consumo_atual, media_historica)

        # 5. Atribuir tokens com base no consumo (passo concreto/hook)
        tokens_atribuidos = self.atribuir_tokens(consumo_atual, media_historica)

        return {
            "email_usuario": self.email_usuario,
            "consumo_atual": consumo_atual,
            "media_historica": media_historica,
            "alerta_necessario": alerta_necessario,
            "mensagem_feedback": mensagem_feedback,
            "tokens_atribuidos": tokens_atribuidos
        }

    # --- Métodos Abstratos (Primitivos) ---

    @abstractmethod
    def calcular_consumo(self, dados_usuario: Dict[str, Any]) -> float:
        """Calcula o consumo específico (e.g., água ou energia) a partir dos dados do usuário."""
        pass

    @abstractmethod
    def obter_media(self) -> float:
        """Obtém a média histórica de consumo ou a meta de consumo para comparação."""
        pass

    @abstractmethod
    def verificar_alerta(self, consumo: float, media: float) -> bool:
        """Verifica se o consumo está acima da média ou meta, indicando a necessidade de alerta."""
        pass

    # --- Métodos Concretos (Hooks e Passos Padrão) ---

    def gerar_alerta(self, alerta: bool, consumo: float, media: float) -> str:
        """Gera a mensagem de alerta ou feedback para o usuário."""
        if alerta:
            excesso = consumo - media
            return (f"ALERTA! Seu consumo ({consumo:.2f}) excedeu a média/meta ({media:.2f}) "
                    f"em {excesso:.2f}. Considere medidas de economia.")
        else:
            economia = media - consumo
            return (f"Parabéns! Seu consumo ({consumo:.2f}) está abaixo da média/meta ({media:.2f}). "
                    f"Você economizou {economia:.2f}!")

    def atribuir_tokens(self, consumo: float, media: float) -> int:
        """
        Hook: Atribui tokens. Implementação padrão: 
        Tokens são atribuídos apenas se o consumo for menor ou igual à média/meta.
        """
        if consumo <= media:
            # Atribui 10 tokens por unidade economizada (exemplo)
            economia = media - consumo
            return int(economia * 10)
        return 0

# ----------------------------------------------------------------------
# Implementações Concretas
# ----------------------------------------------------------------------

class ConsumoAgua(ConsumoTemplate):
    """Implementação concreta para a análise de consumo de Água."""

    def calcular_consumo(self, dados_usuario: Dict[str, Any]) -> float:
        """Simula o cálculo do consumo de água (em litros)."""
        # Exemplo: Acessa o dado 'consumo_agua_litros' do dicionário
        return float(dados_usuario.get("consumo_agua_litros", 0.0))

    def obter_media(self) -> float:
        """Simula a obtenção da média histórica de consumo de água (em litros)."""
        # Exemplo: Média histórica de 15000 litros
        return 15000.0

    def verificar_alerta(self, consumo: float, media: float) -> bool:
        """Verifica se o consumo de água excedeu a média."""
        # Alerta se o consumo for mais de 10% acima da média
        return consumo > media * 1.1

class ConsumoEnergia(ConsumoTemplate):
    """Implementação concreta para a análise de consumo de Energia."""

    def calcular_consumo(self, dados_usuario: Dict[str, Any]) -> float:
        """Simula o cálculo do consumo de energia (em kWh)."""
        # Exemplo: Acessa o dado 'consumo_energia_kwh' do dicionário
        return float(dados_usuario.get("consumo_energia_kwh", 0.0))

    def obter_media(self) -> float:
        """Simula a obtenção da média histórica de consumo de energia (em kWh)."""
        # Exemplo: Média histórica de 300 kWh
        return 300.0

    def verificar_alerta(self, consumo: float, media: float) -> bool:
        """Verifica se o consumo de energia excedeu a média."""
        # Alerta se o consumo for mais de 5% acima da média
        return consumo > media * 1.05

# ----------------------------------------------------------------------
# Exemplo de Uso (Opcional, para testes)
# ----------------------------------------------------------------------

if __name__ == "__main__":
    # Dados de exemplo do usuário
    dados_usuario_agua = {
        "consumo_agua_litros": 16000.0,
        "consumo_energia_kwh": 280.0 # Ignorado por ConsumoAgua
    }
    dados_usuario_energia = {
        "consumo_agua_litros": 14000.0, # Ignorado por ConsumoEnergia
        "consumo_energia_kwh": 320.0
    }

    print("--- Análise de Consumo de Água ---")
    analisador_agua = ConsumoAgua("usuario_teste@email.com")
    resultado_agua = analisador_agua.analisar_consumo(dados_usuario_agua)
    print(f"Resultado: {resultado_agua['mensagem_feedback']}")
    print(f"Tokens Ganhos: {resultado_agua['tokens_atribuidos']}")
    print("-" * 30)

    print("--- Análise de Consumo de Energia ---")
    analisador_energia = ConsumoEnergia("usuario_teste@email.com")
    resultado_energia = analisador_energia.analisar_consumo(dados_usuario_energia)
    print(f"Resultado: {resultado_energia['mensagem_feedback']}")
    print(f"Tokens Ganhos: {resultado_energia['tokens_atribuidos']}")
    print("-" * 30)
