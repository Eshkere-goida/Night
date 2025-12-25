class Projector:
    def __init__(self):
        self.is_on = False
        self.input_source = "HDMI1"
    
    def on(self):
        self.is_on = True
        print("Проектор: ВКЛЮЧЕН")
        print(f"Источник входа: {self.input_source}")
    
    def off(self):
        self.is_on = False
        print("Проектор: ВЫКЛЮЧЕН")
    
    def set_input(self, source):
        self.input_source = source
        print(f"Установлен источник: {source}")