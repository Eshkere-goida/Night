import mysql.connector
from datetime import datetime
from domain.PromoCode import PercentagePromoCode, FixedAmountPromoCode, IPromoCode, PromoCodeRepository

class MySQLPromoCodeRepository(PromoCodeRepository):
    def __init__(self, host, user, password, database):
        self.connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        self.cursor = self.connection.cursor()
        self.create_table()
    
    def create_table(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS promo_codes (
                id INT PRIMARY KEY AUTO_INCREMENT,
                code VARCHAR(50) UNIQUE,
                discount_type ENUM('percentage', 'fixed_amount'),
                discount_value FLOAT,
                min_order_amount FLOAT DEFAULT 0,
                valid_until DATETIME,
                is_active BOOLEAN DEFAULT TRUE,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        self.connection.commit()
    
    def get_promo_code(self, code: str) -> IPromoCode:
        try:
            self.cursor.execute(
                "SELECT code, discount_type, discount_value, min_order_amount, valid_until, is_active FROM promo_codes WHERE code = %s",
                (code,)
            )
            result = self.cursor.fetchone()
            
            if not result or not result[5]:  
                return None
            
            code, discount_type, discount_value, min_order_amount, valid_until, is_active = result
            
            if discount_type == 'percentage':
                return PercentagePromoCode(
                    code=code,
                    discount_percentage=discount_value,
                    valid_until=valid_until
                )
            else:  
                return FixedAmountPromoCode(
                    code=code,
                    discount_amount=discount_value,
                    valid_until=valid_until,
                    min_order_amount=min_order_amount or 0
                )
        except mysql.connector.Error as err:
            print(f"Ошибка при получении промокода: {err}")
            return None
    
    def add_promo_code(self, promo_code: IPromoCode):
        try:
            discount_type = 'percentage' if isinstance(promo_code, PercentagePromoCode) else 'fixed_amount'
            discount_value = promo_code.discount_percentage if isinstance(promo_code, PercentagePromoCode) else promo_code.discount_amount
            min_order_amount = getattr(promo_code, 'min_order_amount', 0)
            valid_until = promo_code.valid_until
            
            self.cursor.execute(
                "INSERT INTO promo_codes (code, discount_type, discount_value, min_order_amount, valid_until) VALUES (%s, %s, %s, %s, %s)",
                (promo_code.get_code(), discount_type, discount_value, min_order_amount, valid_until)
            )
            self.connection.commit()
            print(f"[PromoCodes] Промокод {promo_code.get_code()} добавлен")
        except mysql.connector.Error as err:
            print(f"Ошибка при добавлении промокода: {err}")
    
    def deactivate_promo_code(self, code: str):
        try:
            self.cursor.execute(
                "UPDATE promo_codes SET is_active = FALSE WHERE code = %s",
                (code,)
            )
            self.connection.commit()
            print(f"[PromoCodes] Промокод {code} деактивирован")
        except mysql.connector.Error as err:
            print(f"Ошибка при деактивации промокода: {err}")
    
    def get_all_active_promo_codes(self):
        try:
            self.cursor.execute(
                "SELECT code, discount_type, discount_value FROM promo_codes WHERE is_active = TRUE AND (valid_until IS NULL OR valid_until > NOW())"
            )
            return self.cursor.fetchall()
        except mysql.connector.Error as err:
            print(f"Ошибка при получении промокодов: {err}")
            return []