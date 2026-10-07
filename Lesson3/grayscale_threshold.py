from PIL import Image

def clamp(val: int) -> int:
    if val < 0:
        return 0
    elif val > 255:
        return 255
    return val

def to_grayscale_luminance(input_path: str, output_path: str) -> None:
    img = Image.open(input_path)
    img = img.convert("RGB")
    pixels = img.load()
    height = img.height
    width = img.width
    for y in range(height):
        for x in range(width):
            r,g,b = pixels[x, y]
            gray = int(0.299 * r + 0.587 * g + 0.114 * b)
            pixels[x, y] = (gray, gray, gray)
    
    img.save(output_path,format="PNG")

def apply_contrast(input_path: str, output_path: str, factor: float) -> None:
    img = Image.open(input_path)
    img = img.convert("RGB")
    pixels = img.load()
    height = img.height
    width = img.width
    for y in range(height):
        for x in range(width):
            r,g,b = pixels[x, y]
            new_r = clamp(int(factor * (r - 128) + 128))
            new_g = clamp(int(factor * (g - 128) + 128))
            new_b = clamp(int(factor * (b - 128) + 128))
            pixels[x, y] = (new_r, new_g, new_b)

    img.save(output_path)

def apply_threshold(input_path: str, output_path: str, threshold: int = 128) -> None:
    img = Image.open(input_path)
    img = img.convert("RGB")
    pixels = img.load()
    height = img.height
    width = img.width
    for y in range(height):
        for x in range(width):
            r,g,b = pixels[x, y]
            luminance = int(0.299 * r + 0.587 * g + 0.114 * b)
            if luminance >= threshold:
                pixels[x, y] = (255,255,255)
            else:
                pixels[x, y] = (0,0,0)
    img.save(output_path)
        
