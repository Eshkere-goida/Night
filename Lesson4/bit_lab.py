color_blue = 181
print("Исходный синий цвет (дес):",color_blue)
print("В двоичном виде:         ",bin(color_blue))

last_bit = color_blue & 1
print("Младший бит сейчас равен:    ",last_bit)

MASK_CLEAR = 254
clean_blue = color_blue & MASK_CLEAR

print("\n--- ПОСЛЕ ОЧИСТКИ ---")
print("Результат в дес. виде:       ",clean_blue)
print("Результат вы двоичн. виде:   ", bin(clean_blue))
print("Новый младший бит:        ", clean_blue & 1)
