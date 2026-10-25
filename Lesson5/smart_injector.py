from build_secret_packet import build_secret_packet
from gradient_filter import is_texture_pixel
import os
from PIL import Image
import sys
import argparse

# def get_max_capacity(container_path: str, threshold: int = 12) -> int:
#     img = Image.open(container_path)
#     pixels = img.load()
#     for y in 

def smart_inject(container_path: str, secret_text: str, output_path: str, crypto_key: int) -> None:
    if not os.path.exists(container_path):
        raise FileNotFoundError(f"Файл {container_path} не найден.")

    img = Image.open(container_path)
    img = img.convert("RGB")

    pixels = img.load()
    height = img.height
    width = img.width

    text_bytes = secret_text.encode('utf-8')
    key_bytes = crypto_key.encode('utf-8')
        
    secret_text = bytes(b ^ key_bytes[i % len(key_bytes)] 
    for i, b in enumerate(text_bytes)).decode('iso-8859-1')
    
    packet = build_secret_packet(secret_text)

    packet_iterator = iter(packet)
    MASK_CLEAR_LSB = 254

    for y in range(height):
        for x in range(width):
            
            if is_texture_pixel(pixels, x, y, width):
                try:
                    
                    bit_to_hide = int(next(packet_iterator))
                    
                    r, g, b = pixels[x, y]
                    
                    clean_b = (b & MASK_CLEAR_LSB) | bit_to_hide
                    pixels[x, y] = (r, g, clean_b)
                except StopIteration:
                    
                    break
        else:
            continue
        break

    
    try:
        next(packet_iterator)
      
        raise ValueError("Изображение слишком мало для сохранения этого сообщения.")
    except StopIteration:
      
        pass


    img.save(output_path, format="PNG")

# if __name__ == "__main__":
#     user_secret = input("Введите секретное сообщение для инъекции: ")
#     if user_secret == "":
#         user_secret = "Обед императора в 15.00"

#     path = "container.jpg"
#     output_path = "container_ready.png"
#     smart_inject(path, user_secret, output_path)

#     assert os.path.exists(output_path), "Файл изображения не был создан!"

#     img = Image.open(output_path)

#     assert img.format == "PNG", "Изображение сохранено не в нужном формате!"

#     print("\n[OK] Модуль инъекции работает корректно!")

    
if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(
        description="Стеганографическая утилита для скрытия текста в изображениях с XOR-шифрованием."
    )
    
    
    parser.add_argument("-c", "--container", type=str, help="Путь к исходному изображению-контейнеру")
    parser.add_argument("-o", "--output", type=str, help="Путь для сохранения результата (PNG)")
    parser.add_argument("-s", "--secret", type=str, help="Секретное сообщение для внедрения")
    parser.add_argument("-k", "--key", type=str, help="Ключ шифрования (пароль)")

    args = parser.parse_args()

    
    interactive_mode = len(sys.argv) == 1

    if interactive_mode:
        print("=== Интерактивный режим ===")
        
        path = input("Введите путь к контейнеру (по умолчанию 'container.jpg'): ").strip()
        if not path:
            path = "container.jpg"
            
        output_path = input("Введите путь для сохранения (по умолчанию 'container_ready.png'): ").strip()
        if not output_path:
            output_path = "container_ready.png"
            
        user_secret = input("Введите секретное сообщение (по умолчанию 'Обед императора в 15.00'): ")
        if not user_secret:
            user_secret = "Обед императора в 15.00"
            
        secret_key = input("Введите ключ шифрования (нажмите Enter, если не требуется): ")
    else:
        
        path = args.container if args.container else "container.jpg"
        output_path = args.output if args.output else "container_ready.png"
        user_secret = args.secret if args.secret else "Обед императора в 15.00"
        secret_key = args.key if args.key else ""

    
    try:
        print(f"\n[Запуск] Обработка файла '{path}'...")
        smart_inject(path, user_secret, output_path, crypto_key=secret_key)
        
       
        assert os.path.exists(output_path), "Файл изображения не был создан!"
        img = Image.open(output_path)
        assert img.format == "PNG", "Изображение сохранено не в формате PNG!"
        
        print(f"[OK] Секрет успешно внедрен в '{output_path}'!")
        
    except Exception as e:
        print(f"[Ошибка] Не удалось выполнить инъекцию: {e}")
        sys.exit(1)



from build_secret_packet import build_secret_packet
from gradient_filter import is_texture_pixel

import os
import sys
import argparse
from PIL import Image

# ---------------------------------------------------------------------------
# Константы протокола (совпадают с главой 2 конспекта)
# ---------------------------------------------------------------------------
THRESHOLD     = 12
HEADER_BITS   = 16
EOF_BITS      = 8
EOF_MARKER    = "0" * EOF_BITS
SERVICE_BITS  = HEADER_BITS + EOF_BITS      # 24
MASK_CLEAR_LSB = 0xFE                       # 254 / 0b11111110


# ---------------------------------------------------------------------------
# Глава 5. Аудит ёмкости (fail-fast)
# ---------------------------------------------------------------------------
def get_max_capacity(container_path: str, threshold: int = THRESHOLD) -> int:
    with Image.open(container_path) as img:
        image = img.convert("RGB")
        pixels = image.load()
        width, height = image.size

        count = 0
        for y in range(height):
            for x in range(width):
                if is_texture_pixel(pixels, x, y, width, threshold):
                    count += 1

    return max(0, (count - SERVICE_BITS) // 8)


# ---------------------------------------------------------------------------
# Глава 5. XOR на уровне байтов (обратимо, безопасно для UTF-8)
# ---------------------------------------------------------------------------
def xor_payload(data: bytes, key: bytes) -> bytes:
    if not key:
        return data
    n = len(key)
    return bytes(b ^ key[i % n] for i, b in enumerate(data))


# ---------------------------------------------------------------------------
# Глава 4. Главная функция инъекции
# ---------------------------------------------------------------------------
def smart_inject(container_path: str,
                 secret_text: str,
                 output_path: str,
                 crypto_key: str = "") -> None:

    if not os.path.exists(container_path):
        raise FileNotFoundError(f"Файл {container_path} не найден.")

    # --- 1. Подготовка нагрузки (+ XOR) ---
    text_bytes = secret_text.encode("utf-8")
    key_bytes  = crypto_key.encode("utf-8") if crypto_key else b""
    payload    = xor_payload(text_bytes, key_bytes)

    # --- 2. Fail-fast аудит ёмкости ---
    max_bytes = get_max_capacity(container_path, THRESHOLD)
    if len(payload) > max_bytes:
        raise ValueError(
            f"Ошибка! Сообщение слишком велико ({len(payload)} байт). "
            f"Картинка может вместить максимум {max_bytes} байт "
            f"в текстурных зонах."
        )
    print(f"[+] Аудит пройден: требуется {len(payload)} байт, "
          f"доступно {max_bytes} байт.")

    # --- 3. Сборка пакета (build_secret_packet должен принимать bytes) ---
    packet     = build_secret_packet(payload)
    total_bits = len(packet)
    print(f"[+] Размер пакета: {total_bits} бит "
          f"(16 header + {len(payload) * 8} payload + 8 EOF).")

    # --- 4. Открытие контейнера ---
    with Image.open(container_path) as img:
        image = img.convert("RGB")
    pixels        = image.load()
    width, height = image.size

    # --- 5. Обход, фильтрация и запись ---
    bit_index = 0
    for y in range(height):
        if bit_index >= total_bits:
            break
        for x in range(width):
            if bit_index >= total_bits:
                break
            if not is_texture_pixel(pixels, x, y, width, THRESHOLD):
                continue                                  # гладкая зона
            bit = int(packet[bit_index])
            r, g, b = pixels[x, y]
            pixels[x, y] = (r, g, (b & MASK_CLEAR_LSB) | bit)
            bit_index += 1

    # --- 6. Контроль переполнения ---
    if bit_index < total_bits:
        raise ValueError(
            f"Не хватило текстурных пикселей: записано {bit_index} "
            f"из {total_bits} бит."
        )

    # --- 7. Сохранение строго в PNG ---
    image.save(output_path, format="PNG")
    print(f"[+] Записано бит: {bit_index}/{total_bits}. "
          f"Сохранено: {output_path}")


# ---------------------------------------------------------------------------
# CLI + интерактивный режим
# ---------------------------------------------------------------------------
DEFAULT_MSG = "Обед императора в 15.00"


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Стеганографическая утилита: скрытие текста в изображении "
                    "с контент-адаптивной фильтрацией и XOR-шифрованием."
    )
    parser.add_argument("-c", "--container", type=str,
                        help="Путь к исходному изображению-контейнеру")
    parser.add_argument("-o", "--output", type=str,
                        help="Путь для сохранения результата (PNG)")
    parser.add_argument("-s", "--secret", type=str,
                        help="Секретное сообщение для внедрения")
    parser.add_argument("-k", "--key", type=str,
                        help="Ключ XOR-шифрования (пароль)")
    args = parser.parse_args()

    if len(sys.argv) == 1:                              # интерактивный режим
        print("=== Интерактивный режим ===")
        path = input("Путь к контейнеру (по умолчанию 'container.jpg'): ").strip() \
               or "container.jpg"
        output_path = input("Путь сохранения (по умолчанию 'stego_output.png'): ").strip() \
                      or "stego_output.png"
        user_secret = input("Секретное сообщение (Enter — по умолчанию): ") \
                      or DEFAULT_MSG
        secret_key = input("Ключ XOR (Enter — без шифрования): ")
    else:
        path         = args.container or "container.jpg"
        output_path  = args.output    or "stego_output.png"
        user_secret  = args.secret    or DEFAULT_MSG
        secret_key   = args.key       or ""

    try:
        print(f"\n[Запуск] Обработка '{path}' -> '{output_path}'")
        smart_inject(path, user_secret, output_path, crypto_key=secret_key)

        # --- проверки результата (Глава 4, п.3) ---
        assert os.path.exists(output_path), "Файл стего-изображения не создан!"
        with Image.open(output_path) as check:
            assert check.format == "PNG", \
                f"Ожидался PNG, получен {check.format}"
            assert check.mode == "RGB", \
                f"Ожидался режим RGB, получен {check.mode}"

        print(f"\n[OK] Секрет успешно внедрён в '{output_path}'!")
        print("[OK] Формат PNG, режим RGB подтверждены.")

    except Exception as e:
        print(f"[Ошибка] {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
