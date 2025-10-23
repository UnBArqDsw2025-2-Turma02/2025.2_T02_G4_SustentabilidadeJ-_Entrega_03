from django.db import models

class AcaoSustentavel:
    def __init__(self, tipoAcao):
        self.tipoAcao = tipoAcao
        self.validada = False

    def save(self):
        # Aqui você pode simular o salvamento (ou usar um ORM)
        print(f"Ação '{self.tipoAcao}' salva com sucesso!")
