from PIL import Image

def draw_border(image_path: str, output_path: str, thickness: int, color: tuple[int,int,int]) -> None:
    img = Image.open(image_path)
    rgb_img = img.convert("RGB")
    pixels = rgb_img.load()
    height = rgb_img.height
    width = rgb_img.width
    #top_border
    for y in range(0,thickness):
        for x in range(width):
            pixels[x, y] = color
    #bottom_border
    for y in range(height - thickness, height):
        for x in range(width):
            pixels[x, y] = color
    #left_border
    for x in range(0, thickness):
        for y in range(height):
            pixels[x, y] = color
    #right_border
    for x in range(width - thickness, width):
        for y in range(height):
            pixels[x, y] = color

    rgb_img.save(output_path)

def draw_grid(image_path: str, output_path: str, step: int, color: tuple[int,int,int]) -> None:
    img = Image.open(image_path)
    pixels = img.load()
    height = img.height
    width = img.width
    #horizontal_lines
    for y in range(0,height,step):
        for x in range(width):
            pixels[x, y] = color
    #vertical_lines
    for x in range(0,width,step):
        for y in range(height):
            pixels[x, y] = color
    img.save(output_path)

def generate_tricolor_flag(width: int, height: int, colors: list[tuple[int,int,int]], output_path: str) -> None:
    # colors = [top_color, mid_color, bot_color]
    band = height//3
    canvas = Image.new("RGB",(width, height))
    pixels = canvas.load()
    #top_color
    for x in range(0,width):
        for y in range(0,band):
            pixels[x, y] = colors[0]
    #mid_color
    for x in range(width):
        for y in range(band,2*band):
            pixels[x, y] = colors[1]
    #bot_color
    for x in range(width):
        for y in range(2*band,height):
                pixels[x, y] = colors[2]

    canvas.save(output_path)

import os
from PIL import Image


if __name__ == "__main__":
    # 1. Проверяем генерацию трехцветного флага (300x180)
    flag_file = "test_flag.png"
    # Цвета флага (Белый, Синий, Красный)
    white = (255, 255, 255)
    blue = (0, 57, 166)
    red = (213, 43, 30)

    generate_tricolor_flag(300, 180, [white, blue, red], flag_file)
    assert os.path.exists(flag_file), "Ошибка: файл флага не был создан!"

    # Проверяем контрольные точки каждой полосы флага
    with Image.open(flag_file) as img:
        px = img.load()
        assert (
            px[150, 30] == white
        ), "Ошибка: цвет верхней полосы не совпадает с белым!"
        assert (
            px[150, 90] == blue
        ), "Ошибка: цвет средней полосы не совпадает с синим!"
        assert (
            px[150, 150] == red
        ), "Ошибка: цвет нижней полосы не совпадает с красным!"

    # 2. Проверяем наложение рамки
    bordered_file = "test_bordered.png"
    border_color = (0, 0, 0)  # Черный
    border_thickness = 5

    draw_border(flag_file, bordered_file, border_thickness, border_color)
    assert os.path.exists(bordered_file), "Ошибка: файл с рамкой не сохранен!"

    with Image.open(bordered_file) as img:
        px = img.load()
        # Точки внутри рамки должны стать черными
        assert (
            px[0, 0] == border_color
        ), "Ошибка: угловой пиксель рамки не закрашен!"
        assert (
            px[2, 90] == border_color
        ), "Ошибка: левый край рамки не окрашен корректно!"
        # Внутренний пиксель за пределами толщины рамки должен сохранить цвет флага
        assert (
            px[150, 90] == blue
        ), "Ошибка: содержимое изображения под рамкой повреждено!"

    # 3. Проверяем нанесение координатной сетки
    grid_file = "test_grid.png"
    grid_color = (128, 128, 128)
    grid_step = 50

    draw_grid(flag_file, grid_file, grid_step, grid_color)
    assert os.path.exists(grid_file), "Ошибка: файл с сеткой не создан!"

    with Image.open(grid_file) as img:
        px = img.load()
        # Проверяем пересечение линий сетки (x=50, y=50)
        assert px[50, 50] == grid_color, "Ошибка: линия сетки не нанесена в x=50!"
        # Проверяем точку между линиями сетки (x=25, y=25) — цвет должен остаться белым
        assert px[25, 25] == white, "Ошибка: область между сеткой закрашена ложно!"

    # Очищаем временные файлы
    for temp_path in (flag_file, bordered_file, grid_file):
        if os.path.exists(temp_path):
            os.remove(temp_path)

    print("\n[OK] Все тесты Второй главы пройдены успешно!")
            
                

            
    