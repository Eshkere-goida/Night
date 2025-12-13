from domain.listeners.IEventListener import IEventListener

class DriverDBListener(IEventListener):
    def __init__(self, repository):
        self.repository = repository
    
    def update(self, info: str):
        try:
            parts = info.split(", из ")
            if len(parts) >= 2:
                transport_type = parts[0]
                
                self.repository.cursor.execute("SELECT MAX(id) FROM deliveries")
                last_order_id = self.repository.cursor.fetchone()[0]
                
                if last_order_id:
                    route_info = f"Информация о маршруте: {info}"
                
                    self.repository.save_driver_task(last_order_id, route_info, "ОЖИДАЕТ_НАЗНАЧЕНИЯ")
                else:
                    print("Ошибка: Не найден ID заказа для записи задачи водителя")
                    
        except Exception as e:
            print(f"Ошибка в DriverDBListener: {e}")