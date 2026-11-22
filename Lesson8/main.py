import pygame
from life_core import create_grid, next_generation

WIDTH, HEIGHT = 800, 600
CELL_SIZE = 10
COLS = WIDTH // CELL_SIZE
ROWS = HEIGHT // CELL_SIZE

BG_COLOR = (18, 18, 24)
CELL_COLOR = (0, 255, 136)
GRID_LINE_COLOR = (30, 30, 40)


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("consolas", 16, bold=True)

    fps = 10
    paused = False
    generation = 0
    rule_name = "Классика (B3/S23)"
    born_rules = (3,)
    survive_rules = (2, 3)
    prev_grid = None
    prev_prev_grid = None
    stagnated = False


    grid = create_grid(ROWS, COLS, False)

    glider = [(1, 0), (2, 1), (0, 2), (1, 2), (2, 2)]

    gosper_gun = [
    (0, 4), (0, 5), (1, 4), (1, 5), (10, 4), (10, 5), (10, 6), (11, 3), (11, 7),
    (12, 2), (12, 8), (13, 2), (13, 8), (14, 5), (15, 3), (15, 7), (16, 4), (16, 5),
    (16, 6), (17, 5), (20, 2), (20, 3), (20, 4), (21, 2), (21, 3), (21, 4), (22, 1),
    (22, 5), (24, 0), (24, 1), (24, 5), (24, 6), (34, 2), (34, 3), (35, 2), (35, 3)
    ]

    for gx, gy in gosper_gun:
        grid[gy][gx] = 1

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    grid = create_grid(ROWS, COLS, randomize=True)
                    generation = 0
                    prev_grid = None
                    prev_prev_grid = None
                    stagnated = False

                elif event.key == pygame.K_p:
                    paused = not paused
                elif event.key == pygame.K_c:
                    grid = create_grid(ROWS, COLS, randomize=False)
                    generation = 0
                    prev_grid = None
                    prev_prev_grid = None
                    stagnated = False

                elif event.key == pygame.K_UP:
                    fps = min(60, fps + 5)
                elif event.key == pygame.K_DOWN:
                    fps = max(1 , fps - 5)
                elif event.key == pygame.K_1:
                    born_rules = (3,)
                    survive_rules = (2, 3)
                    rule_name = "Классика (B3/S23)"
                elif event.key == pygame.K_2:
                    born_rules = (3,)
                    survive_rules = (1, 2, 3, 4, 5)
                    rule_name = "Генератор лабиринтов (B3/S12345)"
                elif event.key == pygame.K_3:
                    born_rules = (3,)
                    survive_rules = (0, 1, 2, 3, 4, 5, 6, 7, 8)
                    rule_name = "Рост кристаллов (B3/S012345678)"
                elif event.key == pygame.K_4:
                    born_rules = (1, 3, 5, 7)
                    survive_rules = (1, 3, 5, 7)
                    rule_name = "Репликатор (B1357/S1357)"
            mouse_buttons = pygame.mouse.get_pressed()
            if mouse_buttons[0] or mouse_buttons[2]:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                grid_x = mouse_x // CELL_SIZE
                grid_y = mouse_y // CELL_SIZE
    
                if 0 <= grid_x < COLS and 0 <= grid_y < ROWS:
                    if mouse_buttons[0]:
                        grid[grid_y][grid_x] = 1
                        prev_grid = None
                        prev_prev_grid = None
                        stagnated = False
    
                    elif mouse_buttons[2]:
                        grid[grid_y][grid_x] = 0
                        prev_grid = None
                        prev_prev_grid = None
                        stagnated = False
        screen.fill(BG_COLOR)

        if paused:
            draw_grid_lines(screen)

        population = 0

        for y in range(ROWS):
            for x in range(COLS):
                val = grid[y][x]
                if val != 0:
                    if val > 0:
                        population += 1
                    color = get_cell_color(val)
                    rect = (
                        x * CELL_SIZE,
                        y * CELL_SIZE,
                        CELL_SIZE - 1,
                        CELL_SIZE - 1,
                    )
                    pygame.draw.rect(screen, color, rect)

        if not paused:
            next_g = next_generation(grid, born_rules, survive_rules)

            
            if are_grids_equal(next_g, grid) or are_grids_equal(next_g, prev_grid):
                stagnated = True

            prev_prev_grid = prev_grid
            prev_grid = grid
            grid = next_g
            generation += 1

        
        status = "ПАУЗА" if paused else "АКТИВНА"
        pygame.display.set_caption(
            f"Игра Жизнь | {rule_name} | Поколение: {generation} | Скорость: {fps} FPS | [{status}]"
        )
        draw_hud(screen, font, rule_name, generation, population, fps, paused, stagnated)
        pygame.display.flip()

        clock.tick(fps)

    pygame.quit()


def draw_grid_lines(screen: pygame.Surface) -> None:
    for x in range(0, WIDTH, CELL_SIZE):
        pygame.draw.line(screen, GRID_LINE_COLOR, (x, 0) , (x, HEIGHT))
    for y in range(0, HEIGHT, CELL_SIZE):
        pygame.draw.line(screen, GRID_LINE_COLOR, (0, y), (WIDTH, y))


def get_cell_color(value: int) -> tuple[int, int, int]:
    if value > 0:
        age = min(value, 15)
        t = (age - 1) / 14

        r = int(120 + (0 - 120) * t)
        g = int(255 + (220 - 255) * t)
        b = int(60 + (230 - 60) * t)
        return (r, g, b)

    elif value < 0:
        t = abs(value) / 5.0

        r = int(18 + (0 - 18) * t)
        g = int(18 + (90 - 18) * t)
        b = int(24 + (110 - 24) * t)

        return (r, g, b)

    return BG_COLOR


def draw_hud(
    screen: pygame.Surface,
    font: pygame.font.Font,
    rule_name: str,
    generation: int,
    population: int,
    fps: int,
    paused: bool,
    stagnated: bool = False,
) -> None:
    if paused:
        status = "ПАУЗА"
    elif stagnated:
        status = "СТАГНАЦИЯ"
    else:
        status = "АКТИВНА"
    lines = [
        f"Режим: {rule_name}",
        f"Поколение: {generation} | Популяция: {population}",
        f"Скорость: {fps} FPS | Статус: {status}",
    ]

    padding = 10
    line_height = font.get_linesize()
    max_width = max(font.size(line)[0] for line in lines)

    hud_width = max_width + padding * 2
    hud_height = line_height * len(lines) + padding * 2

    
    hud_surface = pygame.Surface((hud_width, hud_height), pygame.SRCALPHA)
    hud_surface.fill((12, 14, 20, 185))  
    pygame.draw.rect(
        hud_surface, (0, 220, 180, 120), (0, 0, hud_width, hud_height), 1
    )  

    
    for i, text in enumerate(lines):
        color = (255, 190, 60) if (i == 2 and paused) else (225, 240, 245)
        text_surf = font.render(text, True, color)
        hud_surface.blit(text_surf, (padding, padding + i * line_height))

    
    screen.blit(hud_surface, (10, 10))

def are_grids_equal(grid_a: list[list[int]], grid_b: list[list[int]] | None) -> bool:
    if grid_b is None:
        return False

    for y in range(len(grid_a)):
        for x in range(len(grid_a[0])):
            # Считаем клетку живой, если значение > 0
            if (grid_a[y][x] > 0) != (grid_b[y][x] > 0):
                return False
    return True




if __name__ == "__main__":
    main()
