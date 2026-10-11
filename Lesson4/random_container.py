import random
from PIL import Image
import os

def prepare_random_container(input_path: str, output_path: str, secret_key: int, pixels_to_prepare: int) -> None:
    img = Image.open(input_path)
    img = img.convert("RGB")

    width = img.width
    height = img.height
    pixels = img.load()

    random.seed(secret_key)

    for _ in range(pixels_to_prepare):
        rx = random.randint(0, width - 1)
        ry = random.randint(0, height - 1)

        r, g, b = pixels[rx, ry]

        clean_b = b & 254

        pixels[rx, ry] = (r, g, clean_b)

    img.save(output_path, format="PNG")

    
