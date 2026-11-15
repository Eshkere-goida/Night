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
            total += grid[ny][nx]

    return total

import copy

def next_generation(grid: list[list[int]]) -> list[list[int]]:
    rows = len(grid)
    cols = len(grid[0])

    new_grid = copy.deepcopy(grid)

    for y in range(rows):
        for x in range(cols):
            neighbours = count_neighbours(grid, x, y)
            state = grid[y][x]

            if state == 1 and (neighbours < 2 or neighbours > 3):
                new_grid[y][x] = 0

            elif state == 0 and neighbours == 3:
                new_grid[y][x] = 1
            

    return new_grid

if __name__ == "__main__":
    test_world = create_grid(5, 5, False)

    test_world[2][1] = 1
    test_world[2][2] = 1
    test_world[2][3] = 1

    print("Поколение 0: горизонтальная линия")
    for row in test_world:
        print(" ".join(str(cell) for cell in row))

    gen1 = next_generation(test_world)

    print("Поколение 1: вертикальная линия")
    for row in gen1:
        print(" ".join(str(cell) for cell in row))

    assert gen1[1][2] == 1 and gen1[2][2] == 1 and gen1[3][2] == 1, "Ошибка, мигалка не перевернулась!"

    assert gen1[2][1] == 0 and gen1[2][3] == 0, "Ошибка, старые края не умерли!"

    print("[+] Все работает отлично!")
