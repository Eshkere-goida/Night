class Blinds:
    def __init__(self, location="Окно гостиной"):
        self.location = location
        self.is_open = True
    
    def open(self):
        self.is_open = True
        print(f"{self.location}: ОТКРЫТЫ")
    
    def close(self):
        self.is_open = False
        print(f"{self.location}: ЗАКРЫТЫ")