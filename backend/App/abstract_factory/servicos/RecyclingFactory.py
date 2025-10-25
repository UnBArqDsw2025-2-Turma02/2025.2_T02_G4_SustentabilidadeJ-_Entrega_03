from App.abstract_factory.servicos.SustainabilityFactory import (
    SustainabilityFactory, ActionLogger, TokenCalculator, RewardIssuer
)

class RecyclingLogger(ActionLogger):
    def logAction(self, userId: str, payload: dict) -> bool:
        print(f"[RECICLAGEM] Usuário {userId} registrou: {payload}")
        return True


class RecyclingTokenCalculator(TokenCalculator):
    def calculateTokens(self, payload: dict) -> int:
        kg = payload.get("kg", 0)
        return int(kg / 0.5)


class RecyclingRewardIssuer(RewardIssuer):
    def issueReward(self, userId: str, tokens: int) -> str:
        return f"[RECICLAGEM] {tokens} tokens creditados (cupom ecológico emitido)."


class RecyclingFactory(SustainabilityFactory):
    def createLogger(self) -> ActionLogger:
        return RecyclingLogger()

    def createCalculator(self) -> TokenCalculator:
        return RecyclingTokenCalculator()

    def createRewardIssuer(self) -> RewardIssuer:
        return RecyclingRewardIssuer()
