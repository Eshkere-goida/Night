from domain.ITransport import ITransport

class Truck(ITransport):
    def calculate_cost(self, distance: float, weight: float, is_express: bool) -> float:
        price = (distance * 5) + (weight * 2)
        if is_express:
            price *= 1.2
        return price
    
    def get_name(self) -> str:
        return "Грузовик"