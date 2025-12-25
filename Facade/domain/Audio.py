class Audio:
    def __init__(self):
        self.is_on = False
        self.volume = 30
        self.mode = "Стерео"
    
    def on(self):
        self.is_on = True
        print("Аудиосистема: ВКЛЮЧЕНА")
    
    def off(self):
        self.is_on = False
        print("Аудиосистема: ВЫКЛЮЧЕНА")
    
    def set_volume(self, level):
        self.volume = level
        print(f"Громкость установлена на: {level}%")
    
    def set_mode(self, mode):
        self.mode = mode
        print(f"Режим звука: {mode}")