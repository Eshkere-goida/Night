from domain.listeners.IEventListener import IEventListener

class ManagerDBListener(IEventListener):
    def __init__(self, repository):
        self.repository = repository
    
    def update(self, info: str):
        try:
            self.repository.cursor.execute("SELECT MAX(id) FROM deliveries")
            last_order_id = self.repository.cursor.fetchone()[0]
            
            if last_order_id:
                status = "НОВЫЙ_ЗАКАЗ"
                details = f"Событие: {info}"
                
                self.repository.save_manager_log(last_order_id, status, details)
            else:
                print("Ошибка: Не найден ID заказа для записи в лог менеджера")
                
        except Exception as e:
            print(f"Ошибка в ManagerDBListener: {e}")