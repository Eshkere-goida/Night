import telebot
import math
TOKEN = "7981273332:AAFF4OIroh31aiXyct4lhzbxREUrgEmX2Gw"

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(func=lambda message:message.text.lower() == "calc")
def calculator_start(message):
    bot.send_message(message.chat.id ,"Введите операцию(+,-,*,/,//,%,√,^):")
    bot.register_next_step_handler(message,get_operation)

def get_operation(message):
    operation = message.text
    if operation not in ['+','-','*','/','//','%','√','^']:
        bot.send_message(message.chat.id , "Некорректная операция! Попробуйте снова.")
        return
    elif operation == '√':
        bot.send_message(message.chat.id, "Эта операция работает с первым числом.")
    bot.send_message(message.chat.id, "Введите первое число:")
    bot.register_next_step_handler(message,get_first_number,operation)

def get_first_number(message,operation):
    try:
        num1 = float(message.text)
    except ValueError:
        bot.send_message(message.chat.id, "Это не число! Попробуйте снова.")
        return
    if operation == '√':
        result = None
        result = math.sqrt(num1)
        bot.send_message(message.chat.id, f"Результат: {result}")
        return
    bot.send_message(message.chat.id, "Введите второе число:")
    bot.register_next_step_handler(message, get_second_number,operation,num1)

def get_second_number(message,operation,num1):
    try:
        num2 = float(message.text)
    except ValueError:
        bot.send_message(message.chat.id, "Это не число! Попробуйте снова.")
        return
    result = None
    if operation == '+':
        result = num1+num2
    elif operation == '-':
        result = num1-num2
    elif operation == '*':
        result = num1*num2
    elif operation == '/':
        if num2 == 0:
            bot.send_message(message.chat.id,"Деление на ноль невозможно!")
            return
        result = num1/num2
    elif operation == '//':
        if num2 == 0:
            bot.send_message(message.chat.id,"Деление на ноль невозможно!")
            return
        result = num1//num2
    elif operation == '%':
        result = num1%num2
    elif operation == '^':
        result = num1**num2
    elif operation == '√':
            result = math.sqrt(num1)
        
    bot.send_message(message.chat.id, f"Результат: {result}")


bot.polling(non_stop=True)