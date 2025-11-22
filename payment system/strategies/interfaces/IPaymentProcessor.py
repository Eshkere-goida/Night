import abc

class IPaymentProcessor(abc.ABC):
    @abc.abstractmethod
    def pay(self, amount: float) -> bool:
        pass