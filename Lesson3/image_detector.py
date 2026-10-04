from PIL import Image

def inspect_image(file_path: str) -> dict:
    img = Image.open(file_path)
    height = img.height
    width = img.width
    total_pixels = width * height
    raw_ram_bytes = total_pixels * 3
    raw_ram_mb = round(raw_ram_bytes / 1024 * 1024,2)

    info =  {
        "format":img.format,
        "mode": img.mode,
        "width": img.width,
        "height": img.height,
        "total_pixels": total_pixels,
        "raw_ram_bytes": raw_ram_bytes,
        "raw_ram_mb": raw_ram_mb
    }
    return info

def normalize_and_export(input_path: str, output_path: str) -> bool:
    try:
        with Image.open(input_path) as img:
            rgb_img = img.convert("RGB")
            rgb_img.save(output_path, format="PNG")

        return True
    except Exception as e:
        print(f"Ошибка при обработке файла: {e}")
        return False

def create_canvas(width: int, height: int, fill_color: tuple[int, int, int], output_path: str) -> None:
    img = Image.new("RGB",(width,height), fill_color)
    img.save(output_path)


import os
from PIL import Image


if __name__ == "__main__":
    
    test_canvas_path = "test_canvas.png"
    bg_color = (20, 40, 80)
    create_canvas(200, 100, bg_color, test_canvas_path)

    assert os.path.exists(test_canvas_path), "Ошибка: файл холста не был создан на диске!"

    
    info = inspect_image(test_canvas_path)
    print("\nРезультаты анализа метаданных:")
    for key, value in info.items():
        print(f" • {key}: {value}")

    assert info["width"] == 200 and info["height"] == 100, "Ошибка в определении габаритов!"
    assert info["total_pixels"] == 20000, "Ошибка в расчете количества пикселей!"
    assert info["raw_ram_bytes"] == 60000, "Ошибка в расчете веса в памяти (20000 * 3 = 60000 байт)!"
    assert info["mode"] == "RGB", "Ошибка: режим созданного файла должен быть RGB!"

    
    normalized_path = "test_normalized.png"
    assert normalize_and_export(test_canvas_path, normalized_path) is True, "Ошибка при нормализации файла!"

    
    with Image.open(normalized_path) as check_img:
        assert check_img.mode == "RGB", "Ошибка: экспортированный файл не в RGB!"
        assert check_img.size == (200, 100)

    
    for p in (test_canvas_path, normalized_path):
        if os.path.exists(p):
            os.remove(p)

    print("\n[OK] Все тесты Первой главы пройдены успешно!")

    
    
