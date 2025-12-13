from domain.ITransport import ITransport
from services.EventManager import EventManager

class LogisticsService:
    def __init__(self, repository, processor: ITransport):
        self._repository = repository
        self._processor = processor
        self.events = EventManager()

    def calculate_price(self, distance, weight, is_express):
        if not self._repository:
            raise Exception("Ошибка Сервиса: Репозиторий не установлен.")
        if not self._processor:
            raise Exception("Ошибка Сервиса: Процессор не установлен.")
            
        price = self._processor.calculate_cost(distance, weight, is_express)
        return price
    
    def confirm_order(self, transport_type, from_city, to_city, distance, weight, price, is_express, comment):
        try:
            
            self._repository.save_order(transport_type,from_city,to_city,distance,weight,price,is_express,comment)
            
            print(f"✅ Заказ успешно передан в обработку! Спасибо.")
            
            event_info = f"{transport_type}, из {from_city} в {to_city} ({distance}), {weight} кг, {price} руб, Экспресс: {is_express}, комментарий к заказу: {comment}"
            
            self.events.notify(event_info)
        except Exception as e:
            print(f"❌ Произошла непредвиденная ошибка: {e}")