from domain.Sun import Sun

def main():
    
    player1_sun = Sun()
    player2_sun = Sun()

    print("Начальное состояние player2_sun:")
    print(player2_sun.get_status())

    
    player1_sun.add_hours(5)

    print("\nПосле того как Игрок 1 добавил 5 часов:")
    print("Состояние player2_sun:")
    print(player2_sun.get_status())

    print(f"\nПроверка: player1_sun is player2_sun = {player1_sun is player2_sun}")
    print(f"ID player1_sun: {id(player1_sun)}")
    print(f"ID player2_sun: {id(player2_sun)}")

if __name__ == "__main__":
    main()