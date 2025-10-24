import unittest
from backend.App.consumo.servicos.consumo_template import ConsumoAgua, ConsumoEnergia

class TestTemplateMethod(unittest.TestCase):
    """Testes para o padrão Template Method (ConsumoTemplate)."""

    def setUp(self):
        """Prepara dados de teste comuns."""
        self.email = "teste@exemplo.com"
        self.dados_usuario_agua_alta = {"consumo_agua_litros": 18000.0, "consumo_energia_kwh": 0.0} # 20% acima da média de 15000 (alerta > 1.1)
        self.dados_usuario_agua_baixa = {"consumo_agua_litros": 13000.0, "consumo_energia_kwh": 0.0} # Abaixo da média
        self.dados_usuario_energia_alta = {"consumo_agua_litros": 0.0, "consumo_energia_kwh": 320.0} # 6.6% acima da média de 300 (alerta > 1.05)
        self.dados_usuario_energia_baixa = {"consumo_agua_litros": 0.0, "consumo_energia_kwh": 250.0} # Abaixo da média

    def test_consumo_agua_alerta(self):
        """Testa o fluxo de Template Method para ConsumoAgua com alerta."""
        analisador = ConsumoAgua(self.email)
        resultado = analisador.analisar_consumo(self.dados_usuario_agua_alta)

        self.assertTrue(resultado["alerta_necessario"])
        self.assertIn("ALERTA!", resultado["mensagem_feedback"])
        self.assertEqual(resultado["tokens_atribuidos"], 0)
        self.assertEqual(resultado["consumo_atual"], 18000.0)
        self.assertEqual(resultado["media_historica"], 15000.0)

    def test_consumo_agua_economia(self):
        """Testa o fluxo de Template Method para ConsumoAgua com economia."""
        analisador = ConsumoAgua(self.email)
        resultado = analisador.analisar_consumo(self.dados_usuario_agua_baixa)

        self.assertFalse(resultado["alerta_necessario"])
        self.assertIn("Parabéns!", resultado["mensagem_feedback"])
        # Economia de 2000 * 10 tokens = 20000
        self.assertEqual(resultado["tokens_atribuidos"], 20000)
        self.assertEqual(resultado["consumo_atual"], 13000.0)

    def test_consumo_energia_alerta(self):
        """Testa o fluxo de Template Method para ConsumoEnergia com alerta."""
        analisador = ConsumoEnergia(self.email)
        resultado = analisador.analisar_consumo(self.dados_usuario_energia_alta)

        self.assertTrue(resultado["alerta_necessario"])
        self.assertIn("ALERTA!", resultado["mensagem_feedback"])
        self.assertEqual(resultado["tokens_atribuidos"], 0)
        self.assertEqual(resultado["consumo_atual"], 320.0)
        self.assertEqual(resultado["media_historica"], 300.0)

    def test_consumo_energia_economia(self):
        """Testa o fluxo de Template Method para ConsumoEnergia com economia."""
        analisador = ConsumoEnergia(self.email)
        resultado = analisador.analisar_consumo(self.dados_usuario_energia_baixa)

        self.assertFalse(resultado["alerta_necessario"])
        self.assertIn("Parabéns!", resultado["mensagem_feedback"])
        # Economia de 50 * 10 tokens = 500
        self.assertEqual(resultado["tokens_atribuidos"], 500)
        self.assertEqual(resultado["consumo_atual"], 250.0)

if __name__ == '__main__':
    unittest.main()
