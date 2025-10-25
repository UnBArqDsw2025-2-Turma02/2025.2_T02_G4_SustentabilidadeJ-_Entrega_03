from App.abstract_factory.servicos.SustainabilityFactory import (
    SustainabilityFactory, ActionLogger, TokenCalculator, RewardIssuer
)

class PublicTransportLogger(ActionLogger):
    def logAction(self, userId: str, payload: dict) -> bool:
        print(f"[TRANSPORTE] Ação registrada: {payload}")
        return True


class PublicTransportTokenCalculator(TokenCalculator):
    def calculateTokens(self, payload: dict) -> int:
        viagens = payload.get("viagens", 0)
        return viagens * 2


class PublicTransportRewardIssuer(RewardIssuer):
    def issueReward(self, userId: str, tokens: int) -> str:
        return f"[TRANSPORTE] {tokens} tokens convertidos em créditos de mobilidade."


class PublicTransportFactory(SustainabilityFactory):
    def createLogger(self) -> ActionLogger:
        return PublicTransportLogger()

    def createCalculator(self) -> TokenCalculator:
        return PublicTransportTokenCalculator()

    def createRewardIssuer(self) -> RewardIssuer:
        return PublicTransportRewardIssuer()
