from domain.ITransport import ITransport
from domain.Ship import Ship
from domain.Truck import Truck
from domain.Plane import Plane
from domain.ChinaAdapter import ChinaAdapter

class TransportFactory:
    @staticmethod
    def get_transport(type_name: str) -> ITransport:
        if type_name == "road":
            return Truck()
        elif type_name == "sea":
            return Ship()
        elif type_name == "air":
            return Plane()
        elif type_name == "china":
            return ChinaAdapter()
        else:
            raise ValueError("Неизвестный тип транспорта")