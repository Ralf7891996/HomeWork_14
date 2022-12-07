import sqlite3
import pandas


def search_movies(search_title):
    """
    Функция принимает название фильма/сериала и возвращает данные в формате JSON:
    """
    with sqlite3.connect("netflix.db") as connection:
        cur = connection.cursor()
        SQL_query = f"""
                    SELECT title, country, release_year, description, listed_in
                    FROM netflix
                    WHERE title LIKE "%{search_title}%"
                    ORDER BY release_year DESC
                    LIMIT 1
                    """
        try:
            result = cur.execute(SQL_query)
            for i in result:
                dict_movie = {'title': i[0], 'country': i[1], 'release_year': i[2], 'description': i[3], 'genre': i[4]}
            return dict_movie
        except:
            print("В базе данных нет фильмов с таким названием")



def search_movies_to_date(from_date_release, to_date_release):
    """
    Функция принимает две даты и возвращает данные
    о фильмах и сериалах выпущенных в период между этими датами в формате JSON:
    """
    with sqlite3.connect("netflix.db") as connection:
        curs = connection.cursor()
        SQL_query = f"""
                    SELECT  title, release_year
                    FROM netflix
                    WHERE release_year >= {from_date_release} 
                    AND release_year <= {to_date_release}
                    """
        try:
            result = curs.execute(SQL_query).fetchall()
            dict_movies = []
            for movie in result:
                dict_movies.append({'title': movie[0], 'release_year': movie[1]})
            return dict_movies
        except:
            print("Неверный ввод")

def search_movies_by_rating(by_rating):
    """
    Функция принимает одну из категорий: для детей, для семейного просмотра, для взрослых.
    И возвращает список фильмов, которые подходят по рейтингу в формате JSON:
    """
    with sqlite3.connect("netflix.db") as connection:
        curs = connection.cursor()
        if by_rating == 'children':
            SQL_query = f"""
                        SELECT  title, rating, description
                        FROM netflix
                        WHERE rating = 'PG' OR rating = 'G'          
                        """
            try:
                result = curs.execute(SQL_query).fetchall()
                dict_movies = []
                for movie in result:
                    dict_movies.append({'title': movie[0], 'rating': movie[1], 'description': movie[2]})
                return dict_movies
            except:
                print("Неверный ввод")
        elif by_rating == 'family':
            SQL_query = f"""
                        SELECT  title, rating, description
                        FROM netflix
                        WHERE rating = 'PG-13' OR rating = 'G' OR rating = 'PG'             
                        """
            try:
                result = curs.execute(SQL_query).fetchall()
                dict_movies = []
                for movie in result:
                    dict_movies.append({'title': movie[0], 'rating': movie[1], 'description': movie[2]})
                return dict_movies
            except:
                print("Неверный ввод")
        elif by_rating == 'adult':
            SQL_query = f"""
                        SELECT  title, rating, description
                        FROM netflix
                        WHERE rating = 'R' OR rating = 'NC-17'              
                         """
            try:
                result = curs.execute(SQL_query).fetchall()
                dict_movies = []
                for movie in result:
                    dict_movies.append({'title': movie[0], 'rating': movie[1], 'description': movie[2]})
                return dict_movies
            except:
                print("Неверный ввод")
        else:
            return "Неверный ввод"


def search_movies_by_genre(genre):
    """
    Функция принимает жанр фильма.
    И возвращает список фильмов, которые подходят по жанру
    """
    with sqlite3.connect("netflix.db") as connection:
        curs = connection.cursor()
        SQL_query = f"""
                    SELECT  title, description
                    FROM netflix
                    WHERE  listed_in LIKE "%{genre}%"
                    ORDER BY release_year DESC 
                    LIMIT 10
                    """
        try:
            result = curs.execute(SQL_query)
            dict_movies = []
            for movie in result:
                dict_movies.append({'title': movie[0], 'description': movie[1]})
            return dict_movies
        except:
            print("Неверный ввод")



def search_actors(name_1, name_2):
    """
    Функция принимает имена двух актеров.
    И возвращает список актеров, которые снимались вместе с этими актерами больше 2 раз
    """
    with sqlite3.connect("netflix.db") as connection:
        curs = connection.cursor()
        SQL_query = f"""
                    SELECT netflix.cast
                    FROM netflix
                    WHERE netflix.cast LIKE "%{name_1}%" AND netflix.cast LIKE "%{name_2}%" 
                    """
        result = curs.execute(SQL_query).fetchall()
        list_actors = []
        for cast in result:
            for actor in cast:
                list_actors.append(actor)

        list_actors_str = ",".join(list_actors)
        actors = list_actors_str.split(',')
        actors_df = pandas.DataFrame(actors, columns=['Actors'])
        actor_more_2 = actors_df.value_counts().loc[lambda x : x > 2]
        return actor_more_2


def search_movies_by_parametrs(type, data_release, genre):
    """
    Функция принимает три переменные: тип проекта, дата релиза, жанр.
    И возвращает список фильмов, которые подходят по всем параметрам:
    """
    with sqlite3.connect("netflix.db") as connection:
        curs = connection.cursor()
        SQL_query = f"""
                    SELECT  title, description
                    FROM netflix
                    WHERE  listed_in LIKE "%{genre}%" AND netflix.type LIKE "{type}" AND release_year = "{data_release}"
                    """
        try:
            result = curs.execute(SQL_query).fetchall()
            dict_movies = []
            for movie in result:
                dict_movies.append({'title': movie[0], 'description': movie[1]})
            return dict_movies
        except:
            print("Неверный ввод")


