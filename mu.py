import telebot
import requests
from telebot import types

TOKEN = "7981273332:AAFF4OIroh31aiXyct4lhzbxREUrgEmX2Gw"

bot = telebot.TeleBot(TOKEN)
@bot.message_handler(commands=['cat'])
def show_menu(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    btn1 = types.KeyboardButton("🐱")
    markup.add(btn1)

    bot.send_message(message.chat.id , "Выбери действие:", reply_markup=markup)

def get_cat_image():
    url = "https://api.thecatapi.com/v1/images/search"
    response = requests.get(url).json()
    return response[0]["url"]

@bot.message_handler(func=lambda message:message.text.lower() == "🐱")

def send_cat_photo(message):
    cat_image_url = get_cat_image()
    bot.send_photo(message.chat.id , cat_image_url, caption="Вот тебе котик :)")

bot.polling(non_stop=True)
