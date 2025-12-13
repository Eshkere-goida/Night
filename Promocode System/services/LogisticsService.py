from domain.ITransport import ITransport
from services.EventManager import EventManager
from domain.PromoCode import IPromoCode

class LogisticsService:
    def __init__(self, repository, processor: ITransport, promo_repository=None):
        self._repository = repository
        self._processor = processor
        self._promo_repository = promo_repository
        self.events = EventManager()
        self._current_promo_code = None
        self._discount_amount = 0

    def apply_promo_code(self, promo_code_str: str, order_amount: float) -> tuple[bool, str, float]:
        """Применяет промокод к заказу"""
        if not self._promo_repository:
            return False, "Система промокодов недоступна", 0
        
        promo_code = self._promo_repository.get_promo_code(promo_code_str)
        
        if not promo_code:
            return False, "Промокод не найден", 0
        
        if not promo_code.is_valid():
            return False, "Промокод истек или недействителен", 0
        
        original_price = order_amount
        discounted_price = promo_code.apply_discount(original_price)
        discount = original_price - discounted_price
        
        self._current_promo_code = promo_code
        self._discount_amount = discount
        
        return True, f"Применен промокод {promo_code.get_code()}: {promo_code.get_description()}", discounted_price
    
    def clear_promo_code(self):
        """Сбрасывает текущий промокод"""
        self._current_promo_code = None
        self._discount_amount = 0
    
    def calculate_price(self, distance, weight, is_express):
        if not self._repository:
            raise Exception("Ошибка Сервиса: Репозиторий не установлен.")
        if not self._processor:
            raise Exception("Ошибка Сервиса: Процессор не установлен.")
            
        price = self._processor.calculate_cost(distance, weight, is_express)
        return price
    
    def confirm_order(self, transport_type, from_city, to_city, distance, weight, original_price, final_price, discount_amount, promo_code, is_express, comment):
        try:
            self._repository.save_order(
                transport_type, from_city, to_city, distance, weight, 
                original_price, final_price, discount_amount, promo_code, 
                is_express, comment
            )
            
            print(f"✅ Заказ успешно передан в обработку! Спасибо.")
            
            
            promo_info = f", Промокод: {promo_code}" if promo_code else ""
            event_info = f"{transport_type}, из {from_city} в {to_city} ({distance} км), {weight} кг, Цена: {original_price} → {final_price} руб (скидка: {discount_amount} руб){promo_info}, Экспресс: {is_express}, комментарий: {comment}"
            
            self.events.notify(event_info)
            
            
            self.clear_promo_code()
            
        except Exception as e:
            print(f"❌ Произошла непредвиденная ошибка: {e}")