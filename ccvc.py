class Bank:  #4
    def __init__(self, name):
        self.name = name

class Account(Bank):
    def __init__(self, name, balance=0):
        super().__init__(name)
        self.balance = balance

    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            print(f"Депозит на {amount} успешен. Новый баланс: {self.balance}")
        else:
            print("Сумма депозита должна быть положительной")

    def withdraw(self, amount):
        if 0 < amount <= self.balance:
            self.balance -= amount
            print(f"Снятие {amount} успешно. Новый баланс: {self.balance}")
        else:
            print("Недостаточно средств на счете или сумма для снятия некорректна")

class Card(Account):
    def __init__(self, name, balance, card_number):
        super().__init__(name, balance)
        self.card_number = card_number

    def pay(self, amount):
        if self.withdraw(amount):
            print(f"Оплата на {amount} с карты {self.card_number} прошла успешно")

class User:
    def __init__(self, name, account, card):
        self.name = name
        self.account = account
        self.card = card

    def add_money(self, amount):
        self.account.deposit(amount)

    def spend_money(self, amount):
        self.card.pay(amount)


account = Account("Иван Иванов", 1000)
card = Card("Иван Иванов", 1000, "1234 5678 9012 3456")
user = User("Иван Иванов", account, card)

user.add_money(500)
user.spend_money(300)



from abc import ABC,abstractmethod #3

class Product(ABC):
    def __init__(self,price,name):
        self.price = price
        self.name = name
    @abstractmethod
    def get_price(self):
        pass

class Book(Product):
    def get_price(self):
        print(f"Цена {self.name}: {self.price}")

class Clothing(Product):
    def get_price(self):
        print(f"Цена {self.name}: {self.price}")
        
class Electronics(Product):
    def get_price(self):
        print(f"Цена {self.name}: {self.price}")

Roman_Pushkina = Book(1488,"Роман")
Roman_Pushkina.get_price()
Futbolka_Gucci = Clothing(228, "Футболка")
Futbolka_Gucci.get_price()
Chaynik_Philips = Electronics(12184761726471,"Чайник")
Chaynik_Philips.get_price()

    





