from index import Search_film


class Film:
    def __init__(self, title, description, year, special_features, full_name, category_name):
        self.title = title
        self.description = description
        self.year = year
        self.features = special_features
        self.full_name = full_name
        self.category_name = category_name

    def __str__(self):
        return (f'Title : {self.title}\n'
                f'Description : {self.description}\n'
                f'Year : {self.year}\n'
                f'Special Features : {self.features}\n'
                f'Full Name : {self.full_name}\n'
                f'Category : {self.category_name}')


def get_columns(res):
    if res:
        messages = []
        for film_data in res:
            title, description, year, special_features, full_name, category_name = film_data
            film = Film(title, description, year, special_features, full_name, category_name)
            messages.append(str(film))
        return messages
    else:
        return "No results found for your keyword."


def top_query_sort(res):
    sorted_res = sorted(res.items(), key=lambda x: x[1], reverse=True)
    # Вывод в обратном порядке
    # print("Reversed sorted by frequency:", sorted_res[::-1])
    return sorted_res[0:10]


class Search:
    def __init__(self, bot):
        self.bot = bot

    def by_keyword(self, message):
        keyword = message.text
        try:
            res = Search_film.byKeyword(keyword)
            if len(res) == 0:
                self.bot.send_message(message.chat.id, 'no movies found for this request')
            else:
                result_films = get_columns(res)
                for item_film in result_films:
                    self.bot.send_message(message.chat.id, item_film)
        except Exception as err:
            self.bot.send_message(message.chat.id, str(err))

    def in_description(self, message):
        keyword = message.text
        try:
            res = Search_film.byKeywordInDescription(keyword)
            if len(res) == 0:
                self.bot.send_message(message.chat.id, 'no movies found for this request')
            else:
                result_films = get_columns(res)
                for item_film in result_films:
                    self.bot.send_message(message.chat.id, item_film)
        except Exception as err:
            self.bot.send_message(message.chat.id, str(err))

    def by_actor(self, message):
        keyword = message.text
        try:
            res = Search_film.byActor(keyword)
            if len(res) == 0:
                self.bot.send_message(message.chat.id, 'no movies found for this request')
            else:
                result_films = get_columns(res)
                for item_film in result_films:
                    self.bot.send_message(message.chat.id, item_film)
        except Exception as err:
            self.bot.send_message(message.chat.id, str(err))

    def by_genre_and_year(self, message):
        message_value = message.text
        if ',' in message_value:
            keywords = message_value.split(',')
        else:
            keywords = message_value.split(' ')

        if len(keywords) == 2:
            genre, year = keywords[0].strip(), int(keywords[1].strip())
        else:
            genre = keywords[0].strip()
            year = 2010  # Значение по умолчанию

        res = Search_film.byGenreAndYear(genre, year)
        try:
            if len(res) == 0:
                self.bot.send_message(message.chat.id, 'no movies found for this request')
            else:
                result_films = get_columns(res)
                for item_film in result_films:
                    self.bot.send_message(message.chat.id, item_film)
        except Exception as err:
            print(err)
            self.bot.send_message(message.chat.id, str(err))

    def get_top(self, message):
        try:
            res = Search_film.getPopularQueries()
            if not res:
                self.bot.send_message(message.chat.id, "No popular queries found.")
            else:
                sorted_res = top_query_sort(res)
                for item in sorted_res:
                    self.bot.send_message(message.chat.id, f"{item[0]} - {item[1]} times")
        except Exception as err:
            print(f"Произошла ошибка в get_top: {err}")
            self.bot.send_message(message.chat.id, "An error occurred while fetching the top queries.")
