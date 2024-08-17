import logging
import threading

import telebot
from telebot import types

from botUtils import Search
from configs import botKey

bot = telebot.TeleBot(botKey)
# bot.remove_webhook()
# # Включение логирования
logging.basicConfig(level=logging.INFO)
# logging.basicConfig(level=logging.DEBUG)

# Создаем экземпляр класса Search и передаем туда бот
search = Search(bot)

# Словарь для хранения таймеров пользователей
user_timers = {}


# Функция для создания клавиатуры
def create_keyboard():
    keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    button1 = types.KeyboardButton('По ключевому слову')
    button2 = types.KeyboardButton('По жанру & году')
    button3 = types.KeyboardButton('По имени актёра')
    button4 = types.KeyboardButton('По слову в описании')
    button5 = types.KeyboardButton('Top')
    keyboard.add(button1, button2, button3, button4, button5)
    return keyboard


# Функция для скрытия клавиатуры
def hide_keyboard(chat_id):
    bot.send_message(chat_id, "Кнопки были скрыты из-за неактивности.", reply_markup=types.ReplyKeyboardRemove())
    if chat_id in user_timers:
        del user_timers[chat_id]


# Функция для сброса таймера
def reset_timer(chat_id):
    if chat_id in user_timers:
        user_timers[chat_id].cancel()

    timer = threading.Timer(120, hide_keyboard, args=[chat_id])
    user_timers[chat_id] = timer
    timer.start()


# # Определение обработчика для команд /hello и /start
@bot.message_handler(commands=['hello', 'start'])
def send_welcome(message):
    bot.send_message(message.chat.id, "What are we going to do? Maybe you can choose a movie.")
    reset_timer(message.chat.id)  # Сбрасываем таймер при запуске


@bot.message_handler()
def info(message):
    text = message.text.lower()
    print(f"Received message: {text}")
    if text == 'hi':
        bot.send_message(message.chat.id, f'hello, {message.from_user.first_name}')
    elif text == 'Привет':
        bot.reply_to(message, "Привет , как дела?")
    elif text == 'hihi':
        bot.send_message(message.chat.id, f'welcome to hell, {message.from_user.first_name}:-)))')
    elif text == 'id':
        bot.send_message(message.chat.id, f'you id: , {message.from_user.id}')
    elif text == 'durak':
        bot.reply_to(message, f'sam {message.text.upper()}')
    elif text == 'start':
        bot.send_message(message.chat.id, f'Hello, {message.from_user.first_name}. Do you want to select a film? (Yes/No)')
        reset_timer(message.chat.id)  # Сбрасываем таймер при запуске
    elif text in ['yes', 'y', 'ygy']:
        keyboard = create_keyboard()
        bot.send_message(message.chat.id, 'Select the method you want to use for finding a film:', reply_markup=keyboard)
    elif text in ['no', 'n']:
        bot.send_message(message.chat.id, 'Okay, let me know if you need anything else.')
    elif text == 'по ключевому слову':
        bot.send_message(message.chat.id, 'Please enter the keyword you want to search for.')
        bot.register_next_step_handler(message, search.by_keyword)
    elif text == 'По жанру & году'.lower():
        bot.send_message(message.chat.id, 'Please enter the year you want to search for.')
        bot.register_next_step_handler(message, search.by_genre_and_year)
    elif text == 'По слову в описании'.lower():
        bot.send_message(message.chat.id, 'Please enter the year you want to search for.')
        bot.register_next_step_handler(message, search.in_description)
    elif text == 'По имени актёра'.lower():
        bot.send_message(message.chat.id, 'Please enter the year you want to search for.')
        bot.register_next_step_handler(message, search.by_actor)
    elif text == 'Top'.lower():
        bot.send_message(message.chat.id, 'selected query')
        # bot.register_next_step_handler(message, get_top)
        search.get_top(message)
    else:
        bot.reply_to(message, 'i dont understand you')



try:
    print("Бот запускается...")
    bot.polling(non_stop=True)
except KeyboardInterrupt:
    print("Прерывание пользователем. Завершение работы.")
    bot.stop_polling()
except Exception as e:
    print(f"Произошла ошибка: {e}")
    bot.stop_polling()


