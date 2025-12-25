class Lights:
    def __init__(self, location="Гостиная"):
        self.location = location
        self.is_on = False
        self.brightness = 100
    
    def on(self):
        self.is_on = True
        self.brightness = 100
        print(f"Свет в {self.location}: ВКЛЮЧЕН (100%)")
    
    def off(self):
        self.is_on = False
        print(f"Свет в {self.location}: ВЫКЛЮЧЕН")
    
    def dim(self, level=30):
        self.is_on = True
        self.brightness = level
        print(f"Свет в {self.location}: ПРИГЛУШЕН ({level}%)")