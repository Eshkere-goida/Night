from PIL import Image
import os

def prepare_triple_container(input_path: str, output_path: str) -> None:
    img = Image.open(input_path)
    rgb_img = img.convert("RGB")

    width = rgb_img.width
    height = rgb_img.height
    pixels = rgb_img.load()

    MASK_CLEAR_LSB = 192
    
    for y in range(height):
        for x in range(width):
            r, g, b = pixels[x, y]

            clean_r = r & MASK_CLEAR_LSB
            clean_g = g & MASK_CLEAR_LSB
            clean_b = b & MASK_CLEAR_LSB
            
            pixels[x, y] = (clean_r, clean_g, clean_b)

    rgb_img.save(output_path, format="PNG")


if __name__ == "__main__":
  source_image = "cover.jpg"
  result_image = "container_ready.png"

  # Если исходной картинки нет, создаем тестовую автоматически
  if not os.path.exists(source_image):
    Image.new("RGB", (200, 200), (0, 255, 0)).save(source_image)

  # Запуск вашей функции
  prepare_triple_container(source_image, result_image)
  assert os.path.exists(result_image), "Ошибка: файл контейнера не создан!"

  # Автоматический аудит: проверка, что все младшие биты синего канала равны 0
  with Image.open(result_image) as check_img:
    px = check_img.load()
    w, h = check_img.size
    errors = 0

    for y in range(h):
      for x in range(w):
        _, _, b_val = px[x, y]
        if (b_val & 1) != 0:
          errors += 1

    assert errors == 0, f"Ошибка аудита: найдено {errors} неочищенных битов!"

  print("[OK] Контейнер успешно подготовлен, все младшие биты обнулены!")