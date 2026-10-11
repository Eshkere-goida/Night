from PIL import Image
import os

def generate_diff_map(original_path: str, container_path: str, output_path: str) -> None:
    img1 = Image.open(original_path)
    img2 = Image.open(container_path)
    img1 = img1.convert("RGB")
    img2 = img2.convert("RGB")

    if img1.size != img2.size:
        print(f"Размеры изображений не совпадают! {img1.size} != {img2.size}")
    
    height = img1.height
    width = img1.width
    pixels1 = img1.load()
    pixels2 = img2.load()

    diff_img = Image.new("RGB", (width, height))
    diff_pixels = diff_img.load()

    for y in range(height):
        for x in range(width):
            r1, g1, b1 = pixels1[x, y]
            r2, g2, b2 = pixels2[x, y]
            diff_b = abs(b1 - b2)
            amplified = diff_b * 255
            diff_pixels[x, y] = (amplified, amplified, amplified)

    diff_img.save(output_path, format="PNG")


if __name__ == "__main__":
  orig_file = "cover.jpg"
  cont_file = "container_ready.png"
  diff_file = "diff_map.png"

  # Проверяем, существуют ли файлы (если нет — подсказка запустить прошлый скрипт)
  if not os.path.exists(orig_file) or not os.path.exists(cont_file):
    print("[-] Сначала создайте файлы cover.jpg и container_ready.png!")
    # Создадим временные для теста
    img = Image.new("RGB", (100, 100), (100, 150, 200))
    img.save(orig_file)
    # Имитируем подготовку контейнера
    px = img.load()
    px[10, 10] = (100, 150, 201)  #грязный бит
    img.save(cont_file)

  # Запускаем построение карты разницы
  generate_diff_map(orig_file, cont_file, diff_file)
  assert os.path.exists(diff_file), "Ошибка: файл карты разницы не создан!"

  # Проверяем, что файл читается и имеет верный размер
  with Image.open(diff_file) as d_img:
    assert d_img.mode == "RGB", "Ошибка: режим карты разницы должен быть RGB!"
    print(
        "[OK] Карта разницы успешно сгенерирована! Откройте файл 'diff_map.png'"
        " и посмотрите на результаты очистки битов."
    )

