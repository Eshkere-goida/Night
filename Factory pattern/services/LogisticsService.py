from factories.TransportFactory import TransportFactory

class LogisticsService:
    def __init__(self, repository):
        self._repository = repository
        self._processor = None
    
    def set_transport(self, transport_type: str):
        self._processor = TransportFactory.get_transport(transport_type)
    
    def calculate_price(self, distance, weight, is_express):
        if not self._repository:
            raise Exception("Ошибка Сервиса: Репозиторий не установлен.")
        if not self._processor:
            raise Exception("Ошибка Сервиса: Транспорт не выбран.")
            
        price = self._processor.calculate_cost(distance, weight, is_express)
        return price
    
    def confirm_order(self, distance, weight, price, is_express, comment):
        try:
            transport_type = self._processor.get_name()
            self._repository.save(transport_type, distance, weight, price, is_express, comment)
            print(f"✅ Заказ успешно передан в обработку! Спасибо.")
        except Exception as e:
            print(f"❌ Произошла непредвиденная ошибка: {e}")