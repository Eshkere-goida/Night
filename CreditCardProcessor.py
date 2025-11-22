from strategies.interfaces.IPaymentProcessor import IPaymentProcessor

class CreditCardProcessor(IPaymentProcessor):
    def pay(self,amount):
        if amount>5000:
            pin = input("Введите пин-код: ")
            if pin!='1111':
                print("Неверный пин-код")
                return False
            else:
                print(f"Списано {amount} рубля(крупный платеж), из них коммисия {amount*0.02} руб")
                return True
        else:
            print(f"Списано {amount+amount*0.02} рубля, из них коммисия {amount*0.02} руб")
            return True

    

