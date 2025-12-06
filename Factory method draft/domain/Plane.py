from domain.ITransport import ITransport

class Plane(ITransport):
    def calculate_cost(distance:float,weight:float,is_express:bool) -> float:
        price = (distance*50)+(weight*10)
        if is_express:
            price+=5000
            return price
        return price