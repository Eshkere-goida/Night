from PIL import Image

def clamp(val: int) -> int:
    if val < 0:
        return 0
    elif val > 255:
        return 255
    return val

def apply_negative(input_path: str, output_path: str) -> None:
    img = Image.open(input_path)
    rgb_img = img.convert("RGB")
    pixels = rgb_img.load()
    height = rgb_img.height
    width = rgb_img.width
    for y in range(height):
        for x in range(width):
            r,g,b = pixels[x, y]
            new_r = 255-r
            new_g = 255-g
            new_b = 255-b
            pixels[x, y] = (new_r, new_g, new_b)
    rgb_img.save(output_path,format="PNG")

def adjust_brightness(input_path: str, output_path: str, delta: int) -> None:
    img = Image.open(input_path)
    pixels = img.load()
    height = img.height
    width = img.width
    for y in range(height):
        for x in range(width):
            r,g,b = pixels[x, y]
            new_r = clamp(r+delta)
            new_g = clamp(g+delta)
            new_b = clamp(b+delta)
            pixels[x, y] = (new_r,new_g,new_b)
    img.save(output_path)

def isolate_channel(input_path: str, output_path: str, channel: str) -> None:
    img = Image.open(input_path)
    pixels = img.load()
    height = img.height
    width = img.width
    if channel == "R":
        for y in range(height):
            for x in range(width):
                r,g,b = pixels[x, y]
                pixels[x, y]  = (r, 0, 0)
    elif channel == "G":
        for y in range(height):
            for x in range(width):
                r,g,b = pixels[x, y]
                pixels[x, y]  = (0, g, 0)
    elif channel == "B":
        for y in range(height):
            for x in range(width):
                r,g,b = pixels[x, y]
                pixels[x, y]  = (0, 0, b)
    img.save(output_path)

def apply_warm_sunset(input_path: str, output_path: str) -> None:
    img = Image.open(input_path)
    pixels = img.load()
    height = img.height
    width = img.width
    for y in range(height):
        for x in range(width):
            r,g,b = pixels[x, y]
            new_r = clamp(int(r * 1.25))
            new_b = clamp(int(b * 0.8))
            pixels[x, y] = (new_r, g, new_b)
    img.save(output_path)

        
