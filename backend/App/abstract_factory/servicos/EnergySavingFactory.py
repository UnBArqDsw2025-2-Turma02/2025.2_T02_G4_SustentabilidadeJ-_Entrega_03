from App.abstract_factory.servicos.SustainabilityFactory import (
    SustainabilityFactory, ActionLogger, TokenCalculator, RewardIssuer
)

class EnergySavingLogger(ActionLogger):
    def logAction(self, userId: str, payload: dict) -> bool:
        print(f"[ENERGIA] Ação registrada: {payload}")
        return True


class EnergySavingTokenCalculator(TokenCalculator):
    def calculateTokens(self, payload: dict) -> int:
        kwh = payload.get("kwh", 0)
        return min(20, int(kwh))


class EnergySavingRewardIssuer(RewardIssuer):
    def issueReward(self, userId: str, tokens: int) -> str:
        return f"[ENERGIA] {tokens} tokens convertidos em desconto na conta de luz."


class EnergySavingFactory(SustainabilityFactory):
    def createLogger(self) -> ActionLogger:
        return EnergySavingLogger()

    def createCalculator(self) -> TokenCalculator:
        return EnergySavingTokenCalculator()

    def createRewardIssuer(self) -> RewardIssuer:
        return EnergySavingRewardIssuer()
