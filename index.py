from collections import Counter

import mysql

from connector import Connector

# index.pu

arrOfFrequentlyRepeatedQueries = []



class Search_film:

    @staticmethod
    def set_new_query(query):
        setDate = "insert into sakila_top(word_query) values(%s);"
        connection, cursor = Connector.get_db_connection_write()
        # Проверяем, что соединение и курсор успешно созданы
        if connection and cursor:
            try:
                cursor.execute(setDate, (query,))
                connection.commit()  # Подтверждаем изменения
            except mysql.connector.Error as err:  # Обрабатываем ошибки выполнения запроса
                print(f"Ошибка при выполнении запроса: {err}")
                return f"Search_film Ошибка при выполнении запроса: {err}"
            finally:
                Connector.close_db_connection(connection, cursor)
        else:
            print("Не удалось установить соединение с базой данных")
            return "Ошибка подключения к базе данных"



    @staticmethod
    def byKeyword(word):
        Search_film.set_new_query(word)
        selectDate = """
                        select f.title, f.description, f.release_year, f.special_features,
                        concat(a.first_name,' ', a.last_name) as full_name
                        , c.name as category_name
                         from film as f
                        left join film_actor as f2a on f.film_id= f2a.film_id
                        left join actor as a on a.actor_id=f2a.actor_id
                        left join film_category as f2c on f2c.film_id=f.film_id
                        left join category as c on c.category_id=f2c.category_id
                        where f.title like %s
                        or f.description like %s
                        or f.release_year like %s
                        or f.special_features like %s
                        or concat(a.first_name, ' ', a.last_name) like %s
                        or c.name like %s limit 10 ;
                    """
        connection, cursor = Connector.get_db_connection_read()
        if connection and cursor:
            cursor.execute(selectDate, (f'%{word}%', f'%{word}%', f'%{word}%', f'%{word}%', f'%{word}%', f'%{word}%'))
            res = cursor.fetchall()
            # close_db_connection(connection, cursor)
            return res
        else:
            return []

    @staticmethod
    def byActor(word):
        Search_film.set_new_query(word)
        selectDate = """
                        select f.title, f.description, f.release_year, f.special_features,
                        concat(a.first_name,' ', a.last_name) as full_name
                        , c.name as category_name
                         from film as f
                        left join film_actor as f2a on f.film_id= f2a.film_id
                        left join actor as a on a.actor_id=f2a.actor_id
                        left join film_category as f2c on f2c.film_id=f.film_id
                        left join category as c on c.category_id=f2c.category_id
                        where concat(a.first_name, ' ', a.last_name) like %s limit 10 ;
                    """
        connection, cursor = Connector.get_db_connection_read()
        if connection and cursor:
            cursor.execute(selectDate, (f'%{word}%',))
            res = cursor.fetchall()
            # close_db_connection(connection, cursor)
            return res
        else:
            return []

    @staticmethod
    def byKeywordInDescription(word):
        Search_film.set_new_query(word)
        selectDate = """
                        select f.title, f.description, f.release_year, f.special_features,
                        concat(a.first_name,' ', a.last_name) as full_name
                        , c.name as category_name
                         from film as f
                        left join film_actor as f2a on f.film_id= f2a.film_id
                        left join actor as a on a.actor_id=f2a.actor_id
                        left join film_category as f2c on f2c.film_id=f.film_id
                        left join category as c on c.category_id=f2c.category_id
                        where f.description like %s limit 10 ;
                    """
        connection, cursor = Connector.get_db_connection_read()
        if connection and cursor:
            cursor.execute(selectDate, (f'%{word}%',))
            res = cursor.fetchall()
            # close_db_connection(connection, cursor)
            return res
        else:
            return []

    @staticmethod
    def byGenreAndYear(genre, year):
        Search_film.set_new_query(f"Genre: {genre}, Year: {year}")

        selectDate = """
                        select f.title, f.description, f.release_year, f.special_features,
                        concat(a.first_name, ' ', a.last_name) as full_name, c.name as category_name
                        from film as f
                        left join film_actor as f2a on f.film_id = f2a.film_id
                        left join actor as a on a.actor_id = f2a.actor_id
                        left join film_category as f2c on f2c.film_id = f.film_id
                        left join category as c on c.category_id = f2c.category_id
                        where c.name = %s
                        and f.release_year = %s
                        limit 10;
        """

        connection, cursor = Connector.get_db_connection_read()
        if connection and cursor:
            cursor.execute(selectDate, (genre, year))
            res = cursor.fetchall()
            #     close_db_connection(connection, cursor)
            return res
        else:
            return []

    @staticmethod
    def getPopularQueries():
        getDate="""
            select * from sakila_top;
        """
        connection, cursor = Connector.get_db_connection_write()
        if connection and cursor:
            cursor.execute(getDate)
            res = cursor.fetchall()
            #     close_db_connection(connection, cursor)
            return Counter(value for _, value in res)


# close_db_connection(connection, cursor)
