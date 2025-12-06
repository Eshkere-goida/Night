from domain.ITransport import ITransport

class Ship(ITransport):
    def calculate_cost(self, distance: float, weight: float, is_express: bool) -> float:
        return (distance * 0.5) + (weight * 0.1) + 1000
    
    def get_name(self) -> str:
        return "Корабль"