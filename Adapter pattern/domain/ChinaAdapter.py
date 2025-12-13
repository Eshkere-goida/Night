from domain.ITransport import ITransport
from libraries.ChinaPost import ChinaPostApi
class ChinaAdapter(ITransport):
    def calculate_cost(self, distance :float, weight:float, is_express:bool) ->float:
        api = ChinaPostApi()
        api.connect()
        weight*=1000
        price = api.calculate_delivery_cny(weight,distance)
        price*=13
        if is_express:
            price*=1.2
            return price
        else: 
            return price
    def get_name(self) ->str:
        return "ChinaDragonLogistics"
    