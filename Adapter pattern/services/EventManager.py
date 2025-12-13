class EventManager:
    def __init__(self):
        self.subscribers = []
    
    def subscribe(self, person):
        self.subscribers.append(person)
    
    def unsubscribe(self, person):
        self.subscribers.remove(person)
    
    def notify(self, info: str):
        for sub in self.subscribers:
            sub.update(info)