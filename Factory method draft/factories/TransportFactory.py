from domain.ITransport import ITransport
from domain.Ship import Ship
from domain.Truck import Truck
from domain.Plane import Plane
class Fabric:
    def get_transport(type_name:str) ->ITransport:
        try:
            if type_name == "road":
                return Truck()
            if type_name == "sea":
                return Ship()
            if type_name == "air":
                return Plane()
        except ValueError:
            print("Неизвестный тип транспорта")
        
        