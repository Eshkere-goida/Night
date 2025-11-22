import abc

class IPaymentProcessor(abc.ABC):
    @abc.abstractmethod
    def pay(amount:float) -> bool:
        pass