import logging
import telebot
from telebot import types
from botUtils import get_columns, top_query_sort
from configs import botKey
from index import Search_film

bot = telebot.TeleBot(botKey)
# bot.remove_webhook()
# # Включение логирования
logging.basicConfig(level=logging.INFO)
# logging.basicConfig(level=logging.DEBUG)


# # Определение обработчика для команд /hello и /start
@bot.message_handler(commands=['hello', 'start'])
def send_welcome(message):
    bot.send_message(message.chat.id, "What are we going to do? Maybe you can choose a movie.")


def create_keyboard():
    keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    button1 = types.KeyboardButton('По ключевому слову')
    button2 = types.KeyboardButton('По жанру & году')
    button3 = types.KeyboardButton('По имени актёра')
    button4 = types.KeyboardButton('По слову в описании')
    button5 = types.KeyboardButton('Top')
    keyboard.add(button1, button2, button3, button4, button5)
    return keyboard


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
    elif text in ['yes', 'y', 'ygy']:
        keyboard = create_keyboard()
        bot.send_message(message.chat.id, 'Select the method you want to use for finding a film:', reply_markup=keyboard)
    elif text in ['no', 'n']:
        bot.send_message(message.chat.id, 'Okay, let me know if you need anything else.')
    elif text == 'по ключевому слову':
        bot.send_message(message.chat.id, 'Please enter the keyword you want to search for.')
        bot.register_next_step_handler(message, search_by_keyword)
    elif text == 'По жанру & году'.lower():
        bot.send_message(message.chat.id, 'Please enter the year you want to search for.')
        bot.register_next_step_handler(message, search_by_genre_and_year)
    elif text == 'По слову в описании'.lower():
        bot.send_message(message.chat.id, 'Please enter the year you want to search for.')
        bot.register_next_step_handler(message, search_in_description)
    elif text == 'По имени актёра'.lower():
        bot.send_message(message.chat.id, 'Please enter the year you want to search for.')
        bot.register_next_step_handler(message, search_by_actor)
    elif text == 'Top'.lower():
        bot.send_message(message.chat.id, 'selected query')
        # bot.register_next_step_handler(message, get_top)
        get_top(message)
    else:
        bot.reply_to(message, 'i dont understand you')


def search_by_keyword(message):
    keyword = message.text
    print("keyword", keyword)
    try:
        res = Search_film.byKeyword(keyword)
        print("62 line", res)
        if len(res) == 0:
            print("if len(res) == 0")
            bot.send_message(message.chat.id, 'no movies found for this request')
        else:
            result_films = get_columns(res)
            for item_film in result_films:
                bot.send_message(message.chat.id, item_film)
    except Exception as err:
        bot.send_message(message.chat.id, str(err))


def search_in_description(message):
    keyword = message.text
    print("keyword", keyword)
    try:
        res = Search_film.byKeywordInDescription(keyword)
        print("92 line", res)
        if len(res) == 0:
            print("if len(res) == 0")
            bot.send_message(message.chat.id, 'no movies found for this request')
        else:
            result_films = get_columns(res)
            for item_film in result_films:
                bot.send_message(message.chat.id, item_film)
    except Exception as err:
        bot.send_message(message.chat.id, str(err))


def search_by_actor(message):
    keyword = message.text
    print("keyword", keyword)
    try:
        res = Search_film.byActor(keyword)
        print("92 line", res)
        if len(res) == 0:
            print("if len(res) == 0")
            bot.send_message(message.chat.id, 'no movies found for this request')
        else:
            result_films = get_columns(res)
            for item_film in result_films:
                bot.send_message(message.chat.id, item_film)
    except Exception as err:
        bot.send_message(message.chat.id, str(err))


def search_by_genre_and_year(message):
    message_value = message.text
    # print(f"80 Текст сообщения: {message_value}")
    if ',' in message_value:
        keywords = message_value.split(',')
    else:
        keywords = message_value.split(' ')
        # print("86 else: Разделено по пробелам", keywords)

    if len(keywords) == 2:
        # print('89 if len(keywords) == 2')
        genre, year = keywords[0].strip(), int(keywords[1].strip())
    else:
        genre = keywords[0].strip()
        year = 2010  # Значение по умолчанию

    # print(f"Жанр: {genre}, Год: {year}")
    res = Search_film.byGenreAndYear(genre, year)
    # print(f"96 res", res)
    try:
        if len(res) == 0:
            print("100 if len(res) == 0")
            bot.send_message(message.chat.id, 'no movies found for this request')
        else:
            result_films = get_columns(res)
            for item_film in result_films:
                bot.send_message(message.chat.id, item_film)
    except Exception as err:
        print(err)
        bot.send_message(message.chat.id, str(err))


def get_top(message):
    print('Entering get_top function')  # Отладочная информация
    try:
        res = Search_film.getPopularQueries()
        # print("113 line", res)  # Добавьте больше отладочной информации
        if not res:
            bot.send_message(message.chat.id, "No popular queries found.")
        else:
            sorted_res = top_query_sort(res)
            print("sorted_res", sorted_res)
            # bot.send_message(message.chat.id, "\n".join(sorted_res))  # Отправка списка популярных запросов
            for item in sorted_res:
                print(f"{item[0]} - {item[1]} times")
                bot.send_message(message.chat.id, f"{item[0]} - {item[1]} times")
    except Exception as err:
        print(f"Произошла ошибка в get_top: {err}")
        bot.send_message(message.chat.id, "An error occurred while fetching the top queries.")


# ????????
# @bot.message_handler ( func = lambda message : True )
# def echo_all ( message ) :
#     bot.reply_to ( message , message.text.lower() )

try:
    print("Бот запускается...")
    bot.polling(non_stop=True)
except KeyboardInterrupt:
    print("Прерывание пользователем. Завершение работы.")
    bot.stop_polling()
except Exception as e:
    print(f"Произошла ошибка: {e}")
    bot.stop_polling()

# @bot.message_handler(commands=['start'])
# def handle_start(message):
#     bot.send_message(message.chat.id, f'Welcome, {message.from_user.first_name}!')
#
# bot.polling(none_stop=True)
