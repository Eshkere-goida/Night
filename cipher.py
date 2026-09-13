from abc import ABC,abstractmethod

class Cipher(ABC):
    @abstractmethod
    def encrypt(self,text: str) -> str:
        pass
    @abstractmethod
    def decrypt(self,text: str) -> str:
        pass

# # test_cipher = Cipher()

class CaesarCipher(Cipher):
    def __init__(self,shift: int,alphabet: str = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"):
        self.alphabet = alphabet
        self.shift = shift
    def encrypt(self, text: str) -> str:
        result = []
        for char in text:
            is_upper = char.isupper()
            lower_char = char.lower()
            if lower_char in self.alphabet:
                idx = self.alphabet.index(lower_char)
                new_idx = (idx + self.shift) % len(self.alphabet)
                new_char = self.alphabet[new_idx]
                if is_upper:
                    new_char = new_char.upper()
                result.append(new_char)

            else:
                result.append(char)
        
        return("".join(result))

    def decrypt(self, text: str) -> str:
        result = []
        for char in text:
            is_upper = char.isupper()
            lower_char = char.lower()
            if lower_char in self.alphabet:
                idx = self.alphabet.index(lower_char)
                new_idx = (idx - self.shift) % len(self.alphabet)
                new_char = self.alphabet[new_idx]
                if is_upper:
                    new_char = new_char.upper()
                result.append(new_char)
            else:
                result.append(char)

        return("".join(result))


# caesar = CaesarCipher(shift=3)

# original_message = "Привет, Агент 007! Встреча в 18:00."

# encrypted = caesar.encrypt(original_message)

# print("Зашифровано:",encrypted)

# decrypted = caesar.decrypt(encrypted)
# print("Расшифровано:",decrypted)

# assert (
#     decrypted == original_message
# ), "Ошибка: расшифрованный текст не совпадает с оригиналом!"
# print("[ОК] Тест шифра Цезаря пройден успешно!")


class VigenereCipher (Cipher):
    def __init__ (self, key: str, alphabet: str = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"):
        self.key = key.lower()
        self.alphabet = alphabet
    def encrypt(self, text: str) -> str:
        result = []
        key_idx = 0
        for char in text:
            if char.lower() in self.alphabet:
                current_key_char = self.key[key_idx % len(self.key)]
                shift = self.alphabet.index(current_key_char)
                idx = self.alphabet.index(char.lower())
                new_idx = (idx + shift) % len(self.alphabet)
                new_char = self.alphabet[new_idx]
                if char.isupper():
                    new_char = new_char.upper()
                result.append(new_char)
                key_idx+=1
            else:
                result.append(char)
        
        return("".join(result))

    def decrypt(self, text: str) -> str:
        result = []
        key_idx = 0
        for char in text:
            if char.lower() in self.alphabet:
                current_key_char = self.key[key_idx % len(self.key)]
                shift = self.alphabet.index(current_key_char)
                idx = self.alphabet.index(char.lower())
                new_idx = (idx - shift) % len(self.alphabet)
                new_char = self.alphabet[new_idx]
                if char.isupper():
                    new_char = new_char.upper()
                result.append(new_char)
                key_idx+=1
            else:
                result.append(char)

        return("".join(result))


# viginere = VigenereCipher(key="код")

# message = "Атака на рассвете, в 05:00!"

# encrypted = viginere.encrypt(message)
# print("Зашифровано (Виженер):",encrypted)

# decrypted = viginere.decrypt(encrypted)
# print("Расшифровано (Виженер):",decrypted)

# assert (
#     decrypted == message
# ), "Ошибка: расшифрованный текст не совпадает с исходным!"
# print("[ОК] Текс шифра Виженера успешно пройден!")
                
def test_ciphers_pipeline(ciphers: list[Cipher], raw_text: str):
    for cipher in ciphers:
        ciph = cipher
        encrypted = ciph.encrypt(raw_text)
        print("Зашифровано:",encrypted)
        decrypted = ciph.decrypt(encrypted)
        print("Расшифровано:",decrypted)
        assert (
            decrypted == raw_text
        ), "Ошибка: расшифрованный текст не совпадает с исходным!"
        print("[ОК] Текст шифра успешно пройден!")

test_ciphers_pipeline([CaesarCipher(shift=3),VigenereCipher(key="кот"),VigenereCipher(key = "дом")],"Коты Мяоцуйзяо")

        
    
