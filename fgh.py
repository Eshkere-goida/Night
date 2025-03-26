import telebot


TOKEN = "7981273332:AAFF4OIroh31aiXyct4lhzbxREUrgEmX2Gw" 
bot = telebot.TeleBot(TOKEN)

user_data={}

@bot.message_handler(commands=['start'])
def start_handler(message):
    bot.send_message(message.chat.id,'Привет! Я помогу тебе составить резюме. Как тебя зовут?')
    bot.register_next_step_handler(message, ask_name)

def ask_name(message):
    user_data[message.chat.id] = {'name': message.text}
    bot.send_message(message.chat.id, "Отлично! Пожалуйста, отправь свою фотографию.".format(message.text))
    bot.register_next_step_handler(message, ask_photo)

def ask_photo(message):
    if message.photo:
        user_data[message.chat.id]['photo'] = message.photo[-1].file_id
        bot.send_message(message.chat.id, "Спасибо! Когда ты родился? (в формате ДД.ММ.ГГГГ)")
        bot.register_next_step_handler(message, ask_birthdate)
    else:
        bot.send_message(message.chat.id, "Пожалуйста, отправь фотографию.")
        bot.register_next_step_handler(message, ask_photo)

def ask_birthdate(message):
    user_data[message.chat.id]['birthdate'] = message.text
    bot.send_message(message.chat.id, "Расскажи о своем опыте работы.")
    bot.register_next_step_handler(message, ask_experience)

def ask_experience(message):
    user_data[message.chat.id]['experience'] = message.text
    bot.send_message(message.chat.id, "Какие у тебя интересы?")
    bot.register_next_step_handler(message, ask_interests)

def ask_interests(message):
    user_data[message.chat.id]['interests'] = message.text
    bot.send_message(message.chat.id, "Какие у тебя навыки?")
    bot.register_next_step_handler(message, ask_skills)

def ask_skills(message):
    user_data[message.chat.id]['skills'] = message.text
    bot.send_message(message.chat.id, "Чем ты мечтаешь заняться?")
    bot.register_next_step_handler(message, ask_dreams)

def ask_dreams(message):
    user_data[message.chat.id]['dreams'] = message.text
    summary = create_summary(user_data[message.chat.id])
    bot.send_photo(message.chat.id, user_data[message.chat.id]['photo'])
    bot.send_message(message.chat.id, summary)
    user_data[message.chat.id]['photo']
    del user_data[message.chat.id]
    
def create_summary(data):
    return (f"Имя: {data['name']}\n"
            f"Дата рождения: {data['birthdate']}\n"
            f"Опыт: {data['experience']}\n"
            f"Интересы: {data['interests']}\n"
            f"Навыки: {data['skills']}\n"
            f"Мечты: {data['dreams']}")

bot.polling(none_stop=True) 