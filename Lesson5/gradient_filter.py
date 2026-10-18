def is_texture_pixel(pixels, x: int, y: int, width: int, threshold: int = 12) -> bool:
    if x + 1 >= width:
        return False

    r1, g1, b1 = pixels[x, y]

    r2, g2, b2 = pixels[x+1, y]

    gradient = abs(r1 - r2) + abs(g1 - g2)

    return gradient >= threshold

if __name__ == "__main__":
    from PIL import Image

    # --- Тестовое изображение 3x1 пикселя ---
    # (0,0) и (1,0) — гладкая зона, (2,0) — контрастный выброс.
    test_img = Image.new("RGB", (3, 1))
    px = test_img.load()
    px[0, 0] = (100, 150, 200)
    px[1, 0] = (101, 151, 200)  # Разница с (0,0) по R и G равна 2 — гладкая зона
    px[2, 0] = (200,  50, 200)  # Разница с (1,0) по R и G огромная — текстура

    # --- Прогон фильтра ---
    # (0,0): градиент к соседу справа = (101-100) + (151-150) = 2 < 12 → гладкий
    is_p0_ok = is_texture_pixel(px, x=0, y=0, width=3, threshold=12)

    # (1,0): градиент к соседу справа = (200-101) + (50-151) = 99 + 101 = 200 ≥ 12 → текстура
    is_p1_ok = is_texture_pixel(px, x=1, y=0, width=3, threshold=12)

    # --- Диагностический вывод ---
    print(f"[+] Гладкая зона   (0,0): {is_p0_ok}  (ожидалось: False)")
    print(f"[+] Текстурная зона (1,0): {is_p1_ok}  (ожидалось: True)")

    # --- Проверки через assert ---
    assert is_p0_ok is False, (
        "Ошибка: гладкий пиксель ошибочно пропущен фильтром!"
    )
    assert is_p1_ok is True, (
        "Ошибка: контрастный пиксель не распознан фильтром!"
    )

    print("\n[OK] Модуль градиентной фильтрации текстур работает корректно!")