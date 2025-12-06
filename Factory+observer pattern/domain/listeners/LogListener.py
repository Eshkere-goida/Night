from domain.listeners.IEventListener import IEventListener
from datetime import datetime

class LogListener(IEventListener):
    def update(self, info: str):
        try:
            log_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            with open("logistics.log", "a", encoding="utf-8") as f:
                f.write(f"[{log_time}] Событие: {info}\n")
            print(f"[LogFile] Запись в лог-файл выполнена.")
        except Exception as e:
            print(f"Ошибка в LogListener: {e}")