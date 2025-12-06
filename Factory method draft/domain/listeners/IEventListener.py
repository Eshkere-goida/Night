import abc

class IEventListener(abc.ABC):
    @abc.abstractmethod
    def update():
        pass
    