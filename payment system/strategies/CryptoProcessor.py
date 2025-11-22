from strategies.interfaces.IPaymentProcessor import IPaymentProcessor

class CryptoProcessor(IPaymentProcessor):
    def pay(self, amount):
        if amount % 10 != 0:
            print("Число не кратно 10!")
            return False
        else:
            print(f"Списано {amount} рубля, из них комиссия 0 руб")
            return True