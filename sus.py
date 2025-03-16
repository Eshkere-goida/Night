import telebot
from telebot import types
import os
import time 
import requests

TOKEN = "7981273332:AAFF4OIroh31aiXyct4lhzbxREUrgEmX2Gw" 

bot = telebot.TeleBot(TOKEN)
SAVE_PATH = 'img'
if not os.path.exists(SAVE_PATH):
    os.makedirs(SAVE_PATH)




@bot.message_handler(commands=['getButtons'])
def show_menu(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    btn1 = types.KeyboardButton("Получить картинку")
    btn2 = types.KeyboardButton("Сохранить картинку")
    btn3 = types.KeyboardButton("Где ты берешь деньги?")

    markup.add(btn1,btn2,btn3)

    bot.send_message(message.chat.id , "Выбери действие:", reply_markup=markup)


@bot.message_handler(commands=['start1'])
def send_name(message):
    bot.send_message(message.chat.id,'Привет, я сосиска и меня создал ChatGPT')

@bot.message_handler(commands=['start2'])
def send_cat(message):
    cat_image_url = get_cat_image()
    bot.send_photo(message.chat.id , cat_image_url, caption="Вот тебе котик :)")

@bot.message_handler(commands=['GetYouTube'])
def send_youtube(message):
    bot.send_message(message.chat.id,'https://www.youtube.com/watch?v=IxX_QHay02M')

@bot.message_handler(func=lambda message : message.text == "Получить картинку")
def photo(message):
    photo = open('img/photo_2025-03-15_15-32-05.jpg','rb')
    bot.send_photo(message.chat.id,photo)

@bot.message_handler(func=lambda message : message.text == "Сохранить картинку")
def prepare_photo(message):
    bot.send_message(message.chat.id, "Отправьте ваше фото")
@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    file_info = bot.get_file(message.photo[-1].file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    timestamp = int(time.time())
    file_path = os.path.join(SAVE_PATH,f'photo_{message.chat.id}_{timestamp}.jpg')
    with open(file_path,'wb') as new_file:
        new_file.write(downloaded_file)
    bot.reply_to(message,f'Фото сохранено как {file_path}')

@bot.message_handler(func=lambda message: message.text == "Где ты берешь деньги?")
def get_fpi(message):
    bot.reply_to(message,"Вот: https://www.fpifpi.ru/")

@bot.message_handler(func=lambda message: True)
def echo_message(message): 
    bot.reply_to(message, 'Введите одну из предложенных команд: \n '
    '/start1\n'
    'Привет, я сосиска и меня создал ChatGPT\n '
    '/start2\n'
    '*отправляет картинку котика*\n '
    '/GetYouTube \n'
    'UIAUIAUIA кот на YouTube \n'
    '/getButtons \n'
    'кнопки: \n'
    '1) Кнопка ведущая на метод возвращающий картинку из папки в проекте\n '
    '2) Кнопка вопрошающая у пользователя картинку и активирующая метод сохраняющий картинку в папку\n '
    '3) Любой вопрос который ведет к методу с ответом ')

def get_cat_image():
    url = "https://api.thecatapi.com/v1/images/search"
    response = requests.get(url).json()
    return response[0]["url"]



bot.polling(none_stop=True) 