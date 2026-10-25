import os
from PIL import Image


def build_secret_packet(secret_text) -> str:
    
    if isinstance(secret_text, str):
        secret_bytes = secret_text.encode("utf-8")
    else:
        secret_bytes = secret_text
        
    length_val = len(secret_bytes)
    header = bin(length_val)[2:].zfill(16)
    payload_bits = ""
    
    for b in secret_bytes:
        b = bin(b)[2:].zfill(8)
        payload_bits += b
        
    eof_marker = "00000000"
    
    full_packet = header + payload_bits + eof_marker
    
    return full_packet

def is_texture_pixel(pixels, x: int, y: int, width: int, threshold: int = 12) -> bool:
    if x + 1 >= width:
        return False

    r1, g1, b1 = pixels[x, y]

    r2, g2, b2 = pixels[x+1, y]

    gradient = abs(r1 - r2) + abs(g1 - g2)

    return gradient >= threshold

def xor_payload(data: bytes, key: bytes) -> bytes:
    if not key:
        return data
    n = len(key)
    return bytes(b ^ key[i % n] for i, b in enumerate(data))



def unpack_secret_packet(packet_bits: str, xor_key: int = 0) -> str:
    
    header_bits = packet_bits[: 16]
    payload_bits = packet_bits[16 : -8]
    eof_bits = packet_bits[-8 :]

    if eof_bits != "00000000":
        raise ValueError("Ошибка целостности пакета: маркер EOF (00000000) не найден!")

    if len(packet_bits) < 24:
            raise ValueError("Пакет слишком короткий(меньше 24 бит)!")
    
    payload_bytes_len = int(header_bits,2)
    if payload_bytes_len == 0:
        raise ValueError("Контейнер пуст: заголовок длины равен 0 байт!")

    expected_bits = 16 + (payload_bytes_len * 8) + 8
    if len(packet_bits) != expected_bits:
        raise ValueError("Обрыв потока данных: собрано меньше бит, чем указано в заголовке!")

    
    secret_bytes = bytearray()

    for i in range(0, len(payload_bits), 8):
        byte_str = payload_bits[i: i+8]
        byte = int(byte_str, 2)

        byte = xor_payload(byte, xor_key)

        secret_bytes.append(byte)

    try:
        return secret_bytes.decode("utf-8")
    except UnicodeDecodeError:
        raise ValueError("Сбой UTF-8: данные повреждены или неверный ключ XOR!")
    

# if __name__ == "__main__":
#     print("=== Запуск стресс-теста защиты(Edge Cases) ===")

#     empty_packet = "0000000000000000" + "00000000"
#     try:
#         unpack_secret_packet(empty_packet)
#         print("[-] ПРОВАЛ: Скрипт пропустил пустой контейнер!")
#     except ValueError as e:
#         print(f"[+] Защита сработала штатно: {e}")

#     broken_eof_packet = "0000000000000001" + "01000001" + "11111111"
#     try:
#         unpack_secret_packet(broken_eof_packet)
#         print("[-] ПРОВАЛ. Скрипт не заметил отсутствие EOF!")
#     except ValueError as e:
#         print(f"[+] Защита 2 сработала штатно: {e}")

#     truncated_packet = "0000000000110010" + "01000001" + "00000000"
#     try:
#         unpack_secret_packet(truncated_packet)
#         print("[-] ПРОВАЛ. Скрипт не заметил обрыв пакета!")
#     except ValueError as e:
#         print(f"[+] Защита 3 сработала штатно: {e}")


def smart_extract(stego_path: str, threshold: int = 12) -> str:
    
    if not os.path.exists(stego_path):
        raise FileNotFoundError(f"Файл {stego_path} не найден.")

    with Image.open(stego_path) as img:
        img.convert("RGB")
        width, height = img.size
        pixels = img.load()

    extracted_bits = []

    total_bits_needed = None

    for y in range(height):
        for x in range(width):
            if not is_texture_pixel(pixels, x, y, width, threshold):
                continue

            _,_,b = pixels[x, y]

            bit = str(b & 1)

            extracted_bits.append(bit)

            if len(extracted_bits) == 16 and total_bits_needed is None:
                header_str = "".join(extracted_bits)
                payload_len = int(header_str,2)
                if payload_len == 0:
                    raise ValueError("Контейнер пуст: заголовок длины равен 0 байт!")
                total_bits_needed = 16+(payload_len*8)+8

            if total_bits_needed is not None and len(extracted_bits) >= total_bits_needed:
                stop_extraction = True
        if stop_extraction:
            break
    if total_bits_needed is None or len(extracted_bits) < total_bits_needed:
        raise ValueError("Недостаточно текстурных пикселей или в картинке нет тайника!")

    full_packet = "".join(extracted_bits)

    return unpack_secret_packet(full_packet)

if __name__ == "__main__":
    file_path = input("Введите путь файла:").strip()
    if not file_path:
        file_path = "stego_output.png"

    try:
        secret_message = smart_extract(file_path,threshold=12)
        assert isinstance(secret_message, str) and len(secret_message) > 0, "Извлечена пустая строка!"
        print(f"\n[+] ДЕШИФРОВКА УСПЕШНА! Скрытый текст:\n>>> {secret_message}")
    
    except (FileNotFoundError, ValueError) as err:
        print(f"\n[-] СБОЙ ОПЕРАЦИИ: {err}")


    