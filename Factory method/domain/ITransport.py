import abc

class ITransport(abc.ABC):
    @abc.abstractmethod
    def calculate_cost(distance:float,weight:float,is_express:bool) -> float:
        pass
    
    @abc.abstractmethod
    def get_name()->str:
        pass
