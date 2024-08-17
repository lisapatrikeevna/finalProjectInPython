from collections import Counter
from connector import Connector

# index.pu

arrOfFrequentlyRepeatedQueries = []



class Search_film:
    @staticmethod
    def set_new_query(query):
        print("set_new_query", query)
        setDate = "insert into sakila_top(word_query) values(%s);"
        connection, cursor, err = Connector.get_db_connection_write()
        print(setDate)
        if connection and cursor:
            try:
                cursor.execute(setDate,(query,))
                connection.commit()  # Подтверждаем изменения
            except err:
                print(f"Ошибка при выполнении запроса: {err}")
                return f"Search_film Ошибка при выполнении запроса: {err}"
            finally:
                Connector.close_db_connection(connection, cursor)



    @staticmethod
    def byKeyword(word):
        # arrOfFrequentlyRepeatedQueries.append(word)
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
            print("byKeyword arrOfFrequentlyRepeatedQueries", arrOfFrequentlyRepeatedQueries)
            return res
        else:
            print("byKeyword arrOfFrequentlyRepeatedQueries", arrOfFrequentlyRepeatedQueries)
            return []

    @staticmethod
    def byGenreAndYear(genre, year):
        Search_film.set_new_query({'genre': genre, 'year': year})
        # arrOfFrequentlyRepeatedQueries.append(f"{genre}, {year}")
        print(f"byGenreAndYear; Genre: {genre}, Year: {year}")

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
            print("index.py if", f"Genre: {genre}, Year: {year}")
            cursor.execute(selectDate, (genre, year))
            res = cursor.fetchall()
            print("res", res)
            #     close_db_connection(connection, cursor)
            print("arrOfFrequentlyRepeatedQueries", arrOfFrequentlyRepeatedQueries)
            return res
        else:
            print("arrOfFrequentlyRepeatedQueries", arrOfFrequentlyRepeatedQueries)
            return []

    @staticmethod
    def getPopularQueries():
        getDate="""
            select * from sakila_top;
        """
        connection, cursor = Connector.get_db_connection_write()
        if connection and cursor:
            print("index.py 95")
            cursor.execute(getDate)
            res = cursor.fetchall()
            print("res 98", res)
            #     close_db_connection(connection, cursor)
            # print("arrOfFrequentlyRepeatedQueries", arrOfFrequentlyRepeatedQueries)
            return res
        print()
        print(Counter(arrOfFrequentlyRepeatedQueries))
        return Counter(arrOfFrequentlyRepeatedQueries)


# close_db_connection(connection, cursor)
