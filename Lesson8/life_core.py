import random

def create_grid(rows: int, cols: int, randomize: bool = False) -> list[list[int]]:
    if randomize:
        return [
            [random.choice([0, 0, 0, 1]) for _ in range(cols)]
            for _ in range (rows)
        ]

    return [[0 for _ in range(cols)] for _ in range(rows)]

def count_neighbours(grid: list[list[int]], x: int, y: int) -> int:
    rows = len(grid)
    cols = len(grid[0])
    total = 0

    #x + dx % cols 

    for dx in (-1, 0, 1):
        for dy in (-1, 0, 1):
            if dx == 0 and dy == 0:
                continue

            nx = (x + dx) % cols
            ny = (y + dy) % rows
            if grid[ny][nx] > 0:
                total += 1

    return total

import copy

def next_generation(grid: list[list[int]], born_rules: tuple[int, ...] = (3,), survive_rules: tuple[int, ...] = (2, 3), ) -> list[list[int]]:
    rows = len(grid)
    cols = len(grid[0])

    new_grid = copy.deepcopy(grid)

    for y in range(rows):
        for x in range(cols):
            neighbours = count_neighbours(grid, x, y)
            state = grid[y][x]

            if state > 0:
                if neighbours in survive_rules:
                    new_grid[y][x] = state + 1
                else:
                    new_grid[y][x] = -5
            else:
                if neighbours in born_rules:
                    new_grid[y][x] = 1
                elif state < 0:
                    new_grid[y][x] = state + 1

    return new_grid

# if __name__ == "__main__":
#     test_world = create_grid(5, 5, False)

#     test_world[2][1] = 1
#     test_world[2][2] = 1
#     test_world[2][3] = 1

#     print("Поколение 0: горизонтальная линия")
#     for row in test_world:
#         print(" ".join(str(cell) for cell in row))

#     gen1 = next_generation(test_world)

#     print("Поколение 1: вертикальная линия")
#     for row in gen1:
#         print(" ".join(str(cell) for cell in row))

#     gen2 = next_generation(test_world)

#     print("Поколение 2: горизонтальная линия")
#     for row in gen2:
#         print(" ".join(str(cell) for cell in row))

#     assert gen1[1][2] == 1 and gen1[2][2] == 1 and gen1[3][2] == 1, "Ошибка, мигалка не перевернулась!"

#     assert gen1[2][1] == 0 and gen1[2][3] == 0, "Ошибка, старые края не умерли!"

#     print("[+] Все работает отлично!")


if __name__ == "__main__":
    world = create_grid(5, 5, False)

    # Ставим горизонтальную мигалку
    world[2][1] = 1
    world[2][2] = 1
    world[2][3] = 1

    # Прогоняем 6 поколений
    for gen in range(7):
        print(f"--- Поколение {gen} ---")
        for row in world:
            # Форматирование {:2}, чтобы минус не сдвигал столбцы
            print(" ".join(f"{cell:2}" for cell in row))
        world = next_generation(world)
