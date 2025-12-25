class Sun:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.time = 12 
            cls._instance.color = "yellow"
        return cls._instance

    def add_hours(self, h):
        self.time = (self.time + h) % 24

    def get_status(self):
        if 6 <= self.time < 18:
            self.color = "yellow"  
            time_of_day = "день"
        else:
            self.color = "dark blue"  
            time_of_day = "ночь"
        
        return {
            "time": self.time,
            "color": self.color,
            "time_of_day": time_of_day
        }