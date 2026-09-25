import hashlib
import os
import secrets
import sqlite3
import sys

from ciphers import VigenereCipher


def compute_sha256(data: str) -> str:
    
    return hashlib.sha256(data.encode("utf-8")).hexdigest()


def generate_salt(length: int = 16) -> str:
    
    return secrets.token_hex(length)


def hash_password(password: str, salt: str) -> str:
  
    return compute_sha256(password + salt)


def verify_password(password: str, salt: str, stored_hash: str) -> bool:
    
    return hash_password(password, salt) == stored_hash



def init_database(db_name: str = "vault.db") -> None:
    
    with sqlite3.connect(db_name) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS master_auth (
                id INTEGER PRIMARY KEY,
                salt TEXT NOT NULL,
                password_hash TEXT NOT NULL
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS accounts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                service TEXT UNIQUE NOT NULL,
                login TEXT NOT NULL,
                encrypted_password TEXT NOT NULL
            )
        """)


def add_test_account(conn: sqlite3.Connection, service: str, login: str, enc_pwd: str) -> bool:
   
    try:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO accounts (service, login, encrypted_password) VALUES (?, ?, ?)",
            (service, login, enc_pwd)
        )
        return True
    except sqlite3.IntegrityError:
        
        print(f"[-] Сервис '{service}' уже существует.")
        return False


def get_account(conn: sqlite3.Connection, service: str):
   
    cursor = conn.cursor()
    cursor.execute(
        "SELECT login, encrypted_password FROM accounts WHERE service = ?", 
        (service,)
    )
    return cursor.fetchone()  



class PasswordVault:
    def __init__(self, db_name: str = "vault.db"):
        self.db_name = db_name
        init_database(self.db_name)

    def is_first_run(self) -> bool:
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM master_auth")
            count = cursor.fetchone()
            return count == 0

    def set_master_password(self, password: str) -> bool:
        if not self.is_first_run():
            return False
        salt = generate_salt()
        pwd_hash = hash_password(password, salt)
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO master_auth (id, salt, password_hash) VALUES (1, ?, ?)", (salt, pwd_hash))
        return True

    def verify_master_password(self, password: str) -> bool:
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT salt, password_hash FROM master_auth WHERE id = 1")
            row = cursor.fetchone()
            if row is None:
                return False
            salt, stored_hash = row
            return verify_password(password, salt, stored_hash)

    def add_account(self, service: str, login: str, enc_pwd: str) -> bool:
        with sqlite3.connect(self.db_name) as conn:
            return add_test_account(conn, service, login, enc_pwd)

    def get_account(self, service: str):
        with sqlite3.connect(self.db_name) as conn:
            return get_account(conn, service)

    def get_all_services(self) -> list[str]:
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT service FROM accounts ORDER BY service")
            return [row[0] for row in cursor.fetchall()]




def main():
    db_filename = "my_passwords.db"
    vault = PasswordVault(db_filename)
    vigenere_alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"

    if vault.is_first_run():
        print("[-] Хранилище не инициализировано. Задайте Мастер-Пароль.")
        while True:
            master_key = input("Придумайте надежный Мастер-Пароль: ").strip()
            if master_key:
                break
        vault.set_master_password(master_key)
        print("[+] Мастер-пароль успешно сохранен!")
    else:
        authenticated = False
        print("[*] Хранилище заблокировано.")
        for attempt in range(1, 4):
            master_key = input(f"Введите Мастер-Пароль (Попытка {attempt} из 3): ").strip()
            if vault.verify_master_password(master_key):
                authenticated = True
                print("[+] Доступ разрешен!")
                break
            else:
                print("[-] Неверный пароль. Попробуйте снова.")
        
        if not authenticated:
            print("[!] Слишком много неудачных попыток. Программа завершена.")
            sys.exit()

    cipher = VigenereCipher(key=master_key, alphabet=vigenere_alphabet)

    while True:
        print("\n=== Главное меню ===")
        print("1 — Добавить новый аккаунт")
        print("2 — Найти и показать пароль по сервису")
        print("3 — Список всех сохраненных сервисов")
        print("0 — Заблокировать хранилище и выйти")
        
        choice = input("Выберите опцию: ").strip()

        if choice == "1":
            service = input("Введите имя сервиса: ").strip()
            login = input("Введите логин/email: ").strip()
            raw_password = input("Введите пароль: ").strip()

            encrypted_password = cipher.encrypt(raw_password)
            if vault.add_account(service, login, encrypted_password):
                print(f"[+] Аккаунт для '{service}' успешно сохранен!")

        elif choice == "2":
            service = input("Какой сервис найти?: ").strip()
            account_data = vault.get_account(service)

            if account_data:
                login, enc_pwd = account_data
                decrypted_password = cipher.decrypt(enc_pwd)
                print(f"\nДанные для сервиса [{service}]:")
                print(f"  Логин:  {login}")
                print(f"  Пароль: {decrypted_password}")
            else:
                print("[-] Ошибка: Такой сервис не найден в хранилище.")

        elif choice == "3":
            services = vault.get_all_services()
            if services:
                print("\nКаталог сохраненных сервисов:")
                for idx, serv in enumerate(services, start=1):
                    print(f"  {idx}. {serv}")
            else:
                print("[-] Хранилище пока пусто.")

        elif choice == "0":
            print("[!] Хранилище заблокировано. Сессия завершена.")
            break



def run_notebook_chapter3_tests():
    print("--- Запуск официальных тестов Главы 3 ---")
    test_db = "test_vault.db"
    
    if os.path.exists(test_db):
        os.remove(test_db)


    init_database(test_db)

    with sqlite3.connect(test_db) as test_conn:
     
        ok = add_test_account(test_conn, "github", "octocat", "encrypted_secret_hash")
        assert ok is True, "Ошибка: не удалось добавить тестовый аккаунт!"

        
        duplicate = add_test_account(test_conn, "github", "fake_user", "12345")
        assert duplicate is False, "Ошибка: база позволила вставить дубликат сервиса!"

       
        acc = get_account(test_conn, "github")
        assert acc is not None, "Ошибка: сохраненный аккаунт не найден!"
        assert acc[0] == "octocat" and acc[1] == "encrypted_secret_hash", "Ошибка: прочитанные данные не сходятся!"

       
        hack_attempt = get_account(test_conn, "github' OR '1'='1")
        assert hack_attempt is None, "Критическая уязвимость: запрос подвержен SQL-инъекции!"

    print("[OK] Тест третьей главы пройден успешно!")

    
    if os.path.exists(test_db):
        os.remove(test_db)
    print("-----------------------------------------\n")


if __name__ == "__main__":
    
    run_notebook_chapter3_tests()
    
    
    main()
