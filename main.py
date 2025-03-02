import telebot
import math
from telebot import types
TOKEN = "7981273332:AAFF4OIroh31aiXyct4lhzbxREUrgEmX2Gw"

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['calculator'])
def show_menu(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    btn1 = types.KeyboardButton("+")
    btn2 = types.KeyboardButton("-")
    btn3 = types.KeyboardButton("*")
    btn4 = types.KeyboardButton("/")
    btn5 = types.KeyboardButton("//")
    btn6 = types.KeyboardButton("%")
    btn7 = types.KeyboardButton("√")
    btn8 = types.KeyboardButton("^")
    markup.add(btn1,btn2,btn3,btn4,btn5,btn6,btn7,btn8)


    bot.send_message(message.chat.id , "Выбери действие:", reply_markup=markup)


@bot.message_handler(func=lambda message:message.text.lower() == "+")

def get_operation(message):
    bot.send_message(message.chat.id, "Введите первое число:")
    bot.register_next_step_handler(message,get_first_number)

def get_first_number(message):
    try:
        num1 = float(message.text)
    except ValueError:
        bot.send_message(message.chat.id, "Это не число! Попробуйте снова.")
        return
    bot.send_message(message.chat.id, "Введите второе число:")
    bot.register_next_step_handler(message, get_second_number,num1)

def get_second_number(message,num1):
    try:
        num2 = float(message.text)
    except ValueError:
        bot.send_message(message.chat.id, "Это не число! Попробуйте снова.")
        return
    result = None
    
    result = num1 + num2
        
    bot.send_message(message.chat.id, f"Результат: {result}")

@bot.message_handler(func=lambda message:message.text.lower() == "-")

def get_operation1(message):
    bot.send_message(message.chat.id, "Введите первое число:")
    bot.register_next_step_handler(message,get_first_number1)

def get_first_number1(message):
    try:
        num1 = float(message.text)
    except ValueError:
        bot.send_message(message.chat.id, "Это не число! Попробуйте снова.")
        return
    bot.send_message(message.chat.id, "Введите второе число:")
    bot.register_next_step_handler(message, get_second_number1,num1)

def get_second_number1(message,num1):
    try:
        num2 = float(message.text)
    except ValueError:
        bot.send_message(message.chat.id, "Это не число! Попробуйте снова.")
        return
    result = None
    
    result = num1 - num2
        
    bot.send_message(message.chat.id, f"Результат: {result}")


@bot.message_handler(func=lambda message:message.text.lower() == "*")

def get_operation2(message):
    bot.send_message(message.chat.id, "Введите первое число:")
    bot.register_next_step_handler(message,get_first_number2)

def get_first_number2(message):
    try:
        num1 = float(message.text)
    except ValueError:
        bot.send_message(message.chat.id, "Это не число! Попробуйте снова.")
        return
    bot.send_message(message.chat.id, "Введите второе число:")
    bot.register_next_step_handler(message, get_second_number2,num1)

def get_second_number2(message,num1):
    try:
        num2 = float(message.text)
    except ValueError:
        bot.send_message(message.chat.id, "Это не число! Попробуйте снова.")
        return
    result = None
    
    result = num1 * num2
        
    bot.send_message(message.chat.id, f"Результат: {result}")

@bot.message_handler(func=lambda message:message.text.lower() == "/")

def get_operation3(message):
    bot.send_message(message.chat.id, "Введите первое число:")
    bot.register_next_step_handler(message,get_first_number3)

def get_first_number3(message):
    try:
        num1 = float(message.text)
    except ValueError:
        bot.send_message(message.chat.id, "Это не число! Попробуйте снова.")
        return
    bot.send_message(message.chat.id, "Введите второе число:")
    bot.register_next_step_handler(message, get_second_number3,num1)

def get_second_number3(message,num1):
    try:
        num2 = float(message.text)
    except ValueError:
        bot.send_message(message.chat.id, "Это не число! Попробуйте снова.")
        return
    result = None
    
    result = num1 / num2
        
    bot.send_message(message.chat.id, f"Результат: {result}")


@bot.message_handler(func=lambda message:message.text.lower() == "//")

def get_operation4(message):
    bot.send_message(message.chat.id, "Введите первое число:")
    bot.register_next_step_handler(message,get_first_number4)

def get_first_number4(message):
    try:
        num1 = float(message.text)
    except ValueError:
        bot.send_message(message.chat.id, "Это не число! Попробуйте снова.")
        return
    bot.send_message(message.chat.id, "Введите второе число:")
    bot.register_next_step_handler(message, get_second_number4,num1)

def get_second_number4(message,num1):
    try:
        num2 = float(message.text)
    except ValueError:
        bot.send_message(message.chat.id, "Это не число! Попробуйте снова.")
        return
    result = None
    
    result = num1 // num2
        
    bot.send_message(message.chat.id, f"Результат: {result}")

@bot.message_handler(func=lambda message:message.text.lower() == "%")

def get_operation5(message):
    bot.send_message(message.chat.id, "Введите первое число:")
    bot.register_next_step_handler(message,get_first_number5)

def get_first_number5(message):
    try:
        num1 = float(message.text)
    except ValueError:
        bot.send_message(message.chat.id, "Это не число! Попробуйте снова.")
        return
    bot.send_message(message.chat.id, "Введите второе число:")
    bot.register_next_step_handler(message, get_second_number5,num1)

def get_second_number5(message,num1):
    try:
        num2 = float(message.text)
    except ValueError:
        bot.send_message(message.chat.id, "Это не число! Попробуйте снова.")
        return
    result = None
    
    result = num1 % num2
        
    bot.send_message(message.chat.id, f"Результат: {result}")


@bot.message_handler(func=lambda message:message.text.lower() == "^")

def get_operation6(message):
    bot.send_message(message.chat.id, "Введите первое число:")
    bot.register_next_step_handler(message,get_first_number6)

def get_first_number6(message):
    try:
        num1 = float(message.text)
    except ValueError:
        bot.send_message(message.chat.id, "Это не число! Попробуйте снова.")
        return
    bot.send_message(message.chat.id, "Введите второе число:")
    bot.register_next_step_handler(message, get_second_number6,num1)

def get_second_number6(message,num1):
    try:
        num2 = float(message.text)
    except ValueError:
        bot.send_message(message.chat.id, "Это не число! Попробуйте снова.")
        return
    result = None
    
    result = num1 ** num2
        
    bot.send_message(message.chat.id, f"Результат: {result}")

@bot.message_handler(func=lambda message:message.text.lower() == "√")

def get_operation7(message):
    bot.send_message(message.chat.id, "Выбранная операция работает только с первым числом.")
    bot.send_message(message.chat.id, "Введите первое число:")
    bot.register_next_step_handler(message,get_first_number7)

def get_first_number7(message):
    try:
        num1 = float(message.text)
    except ValueError:
        bot.send_message(message.chat.id, "Это не число! Попробуйте снова.")
        return
    result = None
    
    result = math.sqrt(num1)
        
    bot.send_message(message.chat.id, f"Результат: {result}")
    
    
bot.polling(non_stop=True)


