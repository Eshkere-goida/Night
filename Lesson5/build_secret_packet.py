def build_secret_packet(secret_text: str) -> str:
    secret_bytes = secret_text.encode("utf-8")
    length_val = len(secret_bytes)
    header = bin(length_val)[2:].zfill(16)
    payload_bits = ""

    for b in secret_bytes:
        b = bin(b)[2:].zfill(8)
        payload_bits += b

    eof_marker = "00000000"

    full_packet = header + payload_bits + eof_marker

    return full_packet

if __name__ == "__main__":
    # --- Тестовые данные ---
    test_message = "Hi"
    packet = build_secret_packet(test_message)

    # --- Диагностический вывод ---
    print(f"[+] Исходный текст: '{test_message}'")
    print(f"[+] Длина пакета в битах: {len(packet)} бит")
    print(f"[+] Первые 16 бит (заголовок длины): {packet[:16]}")
    print(f"[+] Последние 8 бит (маркер EOF):    {packet[-8:]}")

    # --- Проверки через assert ---
    # Для строки "Hi" длина в байтах равна 2.
    # Итог: 16 бит заголовка + 8 бит ('H') + 8 бит ('i') + 8 бит (EOF) = 40 бит.
    assert len(packet) == 40, (
        f"Ошибка сборки пакета! Ожидалось 40 бит, получено {len(packet)}"
    )
    assert packet[:16] == "0000000000000010", (
        "Ошибка в 16-битном заголовке длины!"
    )
    assert packet[-8:] == "00000000", (
        "Ошибка в маркере конца EOF!"
    )

    print("\n[OK] Модуль сборки пакета данных работает безупречно!")