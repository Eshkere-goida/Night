from PIL import Image
import os

def audit_container(container_path: str) -> dict:
    img = Image.open(container_path)
    img = img.convert("RGB")

    width = img.width
    height = img.height
    img_size = height * width
    pixels = img.load()
    uncleaned_bits = 0

    for y in range(height):
        for x in range(width):
            r, g, b = pixels[x, y]
            if (b & 1) != 0:
                uncleaned_bits += 1
    
    capacity_bytes = img_size // 8
    capacity_kb = round(capacity_bytes / 1024, 2)

    if uncleaned_bits == 0:
        is_safe = True
    else:
        is_safe = False
    
    final_info = {
        "width": width,
        "height": height,
        "total_pixels":  img_size,
        "capacity_bytes" : capacity_bytes,
        "capacity_kb" : capacity_kb,
        "errors_found" : uncleaned_bits,
        "is_safe" : is_safe
    }

    return final_info

if __name__ == "__main__":
  target_container = "container_ready.png"

  
  if not os.path.exists(target_container):
    print("[-] Файл 'container_ready.png' не найден. Создаем тестовый...")
    img = Image.new("RGB", (400, 300), (30, 80, 130))
    
    px = img.load()
    for y in range(300):
      for x in range(400):
        r, g, b = px[x, y]
        px[x, y] = (r, g, b & 254)
    img.save(target_container, "PNG")

  
  report = audit_container(target_container)

  print("\n--- ОТЧЕТ АУДИТА БЕЗОПАСНОСТИ КОНТЕЙНЕРА ---")
  print(f"Разрешение изображения: {report['width']}x{report['height']} px")
  print(f"Всего пикселей в матрице: {report['total_pixels']}")
  print(
      f"Максимум данных для скрытия: {report['capacity_bytes']} байт"
      f" ({report['capacity_kb']} KB)"
  )
  print(f"Количество ошибок (грязных битов): {report['errors_found']}")
  print(f"Статус безопасности (Is Safe): {report['is_safe']}")

  
  assert (
      report["is_safe"] is True
  ), "Ошибка аудита: контейнер содержит неочищенные биты!"
  assert (
      report["capacity_bytes"] > 0
  ), "Ошибка: емкость контейнера равна нулю!"

  print(
      "\n[OK] Аудит завершен успешно! Контейнер полностью готов к внедрению"
      " секретного сообщения."
  )


