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
