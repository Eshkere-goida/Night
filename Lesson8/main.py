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

    fps = 10
    paused = False
    generation = 0

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
            mouse_buttons = pygame.mouse.get_pressed()
            if mouse_buttons[0] or mouse_buttons[2]:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                grid_x = mouse_x // CELL_SIZE
                grid_y = mouse_y // CELL_SIZE

                if 0 <= grid_x < COLS and 0 <= grid_y < ROWS:
                    if mouse_buttons[0]:
                        grid[grid_y][grid_x] = 1
                    elif mouse_buttons[2]:
                        grid[grid_y][grid_x] = 0
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    grid = create_grid(ROWS, COLS, randomize=True)
                    generation = 0
                elif event.key == pygame.K_p:
                    paused = not paused
                elif event.key == pygame.K_c:
                    grid = create_grid(ROWS, COLS, randomize=False)
                    generation = 0
                elif event.key == pygame.K_UP:
                    fps = min(60, fps + 5)
                elif event.key == pygame.K_DOWN:
                    fps = max(1 , fps - 5)
                elif event.key == pygame.K_1:
                    grid = create_grid(ROWS, COLS, randomize=False)
                    generation = 0
                    lwss = [
                        (10, 10), (13, 10),
                        (14, 11),
                        (10, 12), (14, 12),
                        (11, 13), (12, 13), (13, 13), (14, 13),
                    ]
                    for lx, ly in lwss:
                        grid[ly][lx] = 1

        screen.fill(BG_COLOR)
        if paused:
            draw_grid_lines(screen)

        for y in range(ROWS):
            for x in range(COLS):
                if grid[y][x] == 1:
                    rect = (
                        x * CELL_SIZE,
                        y * CELL_SIZE,
                        CELL_SIZE - 1,
                        CELL_SIZE - 1,
                    )
                    pygame.draw.rect(screen, CELL_COLOR, rect)

        if not paused:
            grid = next_generation(grid)
            generation += 1
        
        status = "ПАУЗА" if paused else "АКТИВНА"
        pygame.display.set_caption(
            f"Игра Жизнь | Поколение: {generation} | Скорость: {fps} FPS | [{status}]"
        )
        pygame.display.flip()
        clock.tick(fps)

    pygame.quit()


def draw_grid_lines(screen: pygame.Surface) -> None:
    for x in range(0, WIDTH, CELL_SIZE):
        pygame.draw.line(screen, GRID_LINE_COLOR, (x, 0) , (x, HEIGHT))
    for y in range(0, HEIGHT, CELL_SIZE):
        pygame.draw.line(screen, GRID_LINE_COLOR, (0, y), (WIDTH, y))
if __name__ == "__main__":
    main()