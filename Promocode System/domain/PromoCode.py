from abc import ABC, abstractmethod
from datetime import datetime

class IPromoCode(ABC):
    @abstractmethod
    def apply_discount(self, original_price: float) -> float:
        pass
    
    @abstractmethod
    def is_valid(self) -> bool:
        pass
    
    @abstractmethod
    def get_code(self) -> str:
        pass
    
    @abstractmethod
    def get_description(self) -> str:
        pass


class PercentagePromoCode(IPromoCode):
    def __init__(self, code: str, discount_percentage: float, valid_until: datetime = None):
        self.code = code
        self.discount_percentage = discount_percentage
        self.valid_until = valid_until
    
    def apply_discount(self, original_price: float) -> float:
        discount = original_price * (self.discount_percentage / 100)
        return max(original_price - discount, 0)
    
    def is_valid(self) -> bool:
        if self.valid_until:
            return datetime.now() <= self.valid_until
        return True
    
    def get_code(self) -> str:
        return self.code
    
    def get_description(self) -> str:
        return f"Скидка {self.discount_percentage}%"


class FixedAmountPromoCode(IPromoCode):
    def __init__(self, code: str, discount_amount: float, valid_until: datetime = None, min_order_amount: float = 0):
        self.code = code
        self.discount_amount = discount_amount
        self.valid_until = valid_until
        self.min_order_amount = min_order_amount
    
    def apply_discount(self, original_price: float) -> float:
        if original_price < self.min_order_amount:
            return original_price
        return max(original_price - self.discount_amount, 0)
    
    def is_valid(self) -> bool:
        if self.valid_until:
            return datetime.now() <= self.valid_until
        return True
    
    def get_code(self) -> str:
        return self.code
    
    def get_description(self) -> str:
        return f"Скидка {self.discount_amount} руб."


class PromoCodeRepository(ABC):
    @abstractmethod
    def get_promo_code(self, code: str) -> IPromoCode:
        pass
    
    @abstractmethod
    def add_promo_code(self, promo_code: IPromoCode):
        pass
    
    @abstractmethod
    def deactivate_promo_code(self, code: str):
        pass