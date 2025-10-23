from django.db import models

# authentication/models.py
class Usuario:
    def __init__(self, nome):
        self.nome = nome
        self.saldoTokens = 0

    def save(self):
        print(f"Usuário {self.nome} com saldo {self.saldoTokens} salvo!")
