from domain.Lights import Lights
from domain.Projector import Projector
from domain.Audio import Audio
from domain.Blinds import Blinds

class HomeTheaterFacade:
    def __init__(self):
        self.lights = Lights("Гостиная")
        self.projector = Projector()
        self.audio = Audio()
        self.blinds = Blinds("Окно гостиной")
        
        print("Домашний кинотеатр инициализирован")
    
    def watch_movie(self, movie_input="HDMI1", volume=50):
        
        print("АКТИВАЦИЯ РЕЖИМА КИНОТЕАТРА")
        
        
        print("\nПодготовка к просмотру фильма:")
        self.blinds.close()           
        self.lights.dim(10)           
        self.projector.set_input(movie_input)  
        self.projector.on()           
        self.audio.on()               
        self.audio.set_volume(volume) 
        self.audio.set_mode("Объемный звук 5.1")
        
        print(f"\n✅ Режим кинотеатра активирован!")
        print(f"   Громкость: {volume}% | Источник: {movie_input}")
    
    def end_movie(self):
        
        
        print("\nЗавершение сеанса:")
        self.projector.off()          
        self.audio.off()              
        self.lights.on()              
        self.blinds.open()           
        
        print("\n✅ Режим кинотеатра завершен!")
    
    