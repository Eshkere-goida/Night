import abc

class IEventListener(abc.ABC):
    @abc.abstractmethod
    def update(self, info: str):
        pass