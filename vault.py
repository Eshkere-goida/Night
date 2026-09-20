import hashlib
import secrets
import sqlite3
import os


class PasswordVault():
    def __init__(self,db_name: str = "vault.db"):
        self.db_name = db_name
        self._init_db() = init_database(db_name)

    def is_first_run(self) ->bool:
        

        
def init_database(db_name:str = "vault.db") -> None:
    with sqlite3.connect(db_name) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS master_auth (id INTEGER PRIMARY KEY AUTOINCREMENT, salt TEXT NOT NULL, password_hash TEXT NOT NULL)"
        )
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS accounts (id INTEGER PRIMARY KEY AUTOINCREMENT, service TEXT UNIQUE NOT NULL, login TEXT NOT NULL, encrypted_password TEXT NOT NULL)"
        )
        

def add_test_account(conn: sqlite3.Connection, service: str,login: str, enc_pwd: str) ->bool:
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO accounts (service,login,encrypted_password) VALUES (?,?,?)",(service,login,enc_pwd)
        )
        return True
    except sqlite3.IntegrityError:
        print(f"[-] сервиc {service} уже существует в бд")
        return False

def get_account(conn:sqlite3.Connection,service:str):
    cursor = conn.cursor()
    cursor.execute(
        "SELECT login,encrypted_password FROM accounts WHERE service = ?",(service,)
    )
    data_tuple = cursor.fetchone()
    if data_tuple:     
        return data_tuple
    else: return None


# def generate_salt(length:int = 16) -> str:
#     salt = secrets.token_hex(length)
#     return salt

# def hash_password(password:str,salt:str) ->str:
#     stored_hash = compute_sha256(password+salt)
#     return stored_hash

# def verify_password(password: str, salt: str, stored_hash: str) -> bool:
#     if hash_password(password,salt) == stored_hash: 
#         return True
#     else: 
#         return False
# def compute_sha256(data:str) -> str:
#     byte_data = data.encode("utf-8")
#     hash_obj = hashlib.sha256(byte_data)
#     hex_digest = hash_obj.hexdigest()
#     return hex_digest

# def avalanche_demonstration():
#     str1 = "Password123"
#     str2 = "Password124"
#     hash_1 = compute_sha256(str1)
#     hash_2 = compute_sha256(str2)
#     if len(hash_1) == len(hash_2):
#         print("Длины хэшей равны:",len(hash_1),'=',len(hash_2))
#         print(hash_1)
#         print(hash_2)
#     else:
#         print("Произошла ошибка")

if __name__ == "__main__":
    # test_hash = compute_sha256("admin")
    # print(f"SHA-256('admin'):\n{test_hash}\n")
    # assert len(test_hash) == 64, "Ошибка"
    # assert test_hash == "8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918",(
    #     "Ошибка в хэшировании"
    # )

    # avalanche_demonstration()
    # print("[OK] Тест пройден успешно")
    # salt_1 = generate_salt()
    # salt_2 = generate_salt()

    # assert (
    #     len(salt_1) == 32
    # ), "Ошибка длины соли!"
    # assert salt_1 != salt_2, "Ошибка генерации соли"

    # raw_pwd = "SuperSecretPassword_2026"
    # hash_1 = hash_password(raw_pwd,salt_1)
    # hash_2 = hash_password(raw_pwd,salt_2)

    # assert (
    #     hash_1 != hash_2
    # ), "Ошибка генерации паролей"

    # assert verify_password(raw_pwd,salt_1,hash_1) is True, (
    #     "Ошибка при проверке верного пароля"
    # )

    # assert verify_password("WrongPassword",salt_1,hash_1) is False, (
    #     "Ошибка при проверке неверного пароля"
    # )

    # print("[OK] Тест 2 пройден успешно")
    # test_db = "test_vault.db"
    # if os.path.exists(test_db):
    #     os.remove(test_db)

    # init_database(test_db)

    # with sqlite3.connect(test_db) as test_conn:
    #     ok = add_test_account(
    #         test_conn,"github","octocat","encrypted_secret_hash"
    #     )
    #     assert ok is True, "Не удалось создать тестовый аккаунт"

    #     duplicate = add_test_account(test_conn,"github","fake_user","12345")
    #     assert duplicate is False, (
    #         "База данный позволила вставить дубликат сервиса"
    #     )

    #     acc = get_account(test_conn,"github")
    #     assert acc is not None, "Сохраненный аккаунт не найден"
    #     assert acc[0]=="octocat" and acc[1] == "encrypted_secret_hash",(
    #         "Прочитанные данные не сходятся"
    #     )

    #     hack_attempt = get_account(test_conn,"github' OR '1'='1")
    #     assert hack_attempt is None, (
    #         "Запрос подвержен SQL инъекции"
    #     )
    #     print("[OK] Тест 3 пройден успешно")

    # test_conn.close()

    # if os.path.exists(test_db):
    #     os.remove(test_db)

