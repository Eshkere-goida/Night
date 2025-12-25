from services.HomeTheaterFacade import HomeTheaterFacade

class RemoteController:
    def __init__(self):
        self.theater = HomeTheaterFacade()
    
    def run(self):
        
       
      
        
        while True:
            print("ГЛАВНОЕ МЕНЮ:")
            
            print("1.Смотреть кино")
            print("2.Закончить просмотр")
            print("3.Выключение")
            
            choice = input("\nВыберите опцию (1-3): ").strip()
            
            if choice == "1":
                movie_source = input("Источник (HDMI1/HDMI2/Blu-ray) [HDMI1]: ").strip()
                if not movie_source:
                    movie_source = "HDMI1"
                
                volume = input("Громкость (20-80) [50]: ").strip()
                if volume.isdigit():
                    volume = int(volume)
                else:
                    volume = 50
                
                self.theater.watch_movie(movie_source, volume)
            
            elif choice == "2":
                self.theater.end_movie()
        

            elif choice == "3":
                print("\nВыключение системы...")
                print("Спасибо за использование Умного Дома!")
                break
            
            else:
                print("Неверный выбор. Попробуйте снова.")
    
    
        
        