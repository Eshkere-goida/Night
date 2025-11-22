from strategies.interfaces.IPaymentProcessor import IPaymentProcessor

class PaymentService:
    def __init__(self, repository, processor: IPaymentProcessor):
        self._repository = repository
        self._processor = processor

    def process_order(self, amount):
        if not self._repository:
            raise Exception("Ошибка Сервиса: Репозиторий не установлен.")
        if not self._processor:
            raise Exception("Ошибка Сервиса: Процессор не установлен.")
            
        success = self._processor.pay(amount)
        
        if success:
            status = "SUCCESS"   
        else:
            success = "FAILED"
        method_name = self._processor.__class__.__name__
        
        self._repository.add_transaction(amount, method_name, status)
        
        if success:
            print(f"✅ Платеж на сумму {amount} руб. успешно обработан!")
        else:
            print(f"❌ Платеж на сумму {amount} руб. не прошел.")
            
        return success