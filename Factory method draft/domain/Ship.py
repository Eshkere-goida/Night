from domain.ITransport import ITransport

class Ship(ITransport):
    def calculate_cost(distance:float,weight:float,is_express:bool) -> float:
        price = (distance*0.5)+(weight*0.1) + 1000
        if is_express:
            return price
        return price