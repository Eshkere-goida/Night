from domain.ITransport import ITransport

class LogisticsService:
    def __init__(self, repository, processor: ITransport):
        self._repository = repository
        self._processor = processor

    def calculate_price(self,distance,weight,is_express):
        if not self._repository:
            raise Exception("Ошибка Сервиса: Репозиторий не установлен.")
        if not self._processor:
            raise Exception("Ошибка Сервиса: Процессор не установлен.")
            
        price = self._processor.calculate_cost(distance,weight,is_express)
        
        
        
        
        return price
    def confirm_order(self, distance,weight,price,is_express):
        try:
            comment = input("Оставьте комментарий к заказу: ")
            self._repository.save(self, distance,weight,price,is_express,comment)
            print(f"✅ Заказ успешно передан в обработку! Спасибо.")
        except Exception as e:
            print(f"❌ Произошла непредвиденная ошибка: {e}")
        