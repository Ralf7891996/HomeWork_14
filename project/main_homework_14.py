from flask import Flask, jsonify

from project.utils_homework_14 import search_movies, search_movies_to_date, search_movies_by_rating, \
    search_movies_by_genre

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True


# Реализуем view для поиска фильма по названию
@app.route("/movie/<title>")
def movie(title):
    movie_title = search_movies(title)
    return jsonify(movie_title)


# Реализуем view для поиска фильма по датам производства
@app.route("/movies/<int:year>/to/<int:to_year>")
def movies_year(year, to_year):
    movies = search_movies_to_date(year, to_year)
    return jsonify(movies)


# Реализуем view для поиска фильма по возрастному рейтингу
@app.route("/rating/<rating>")
def movies_by_rating(rating):
    movies = search_movies_by_rating(rating)
    return jsonify(movies)


# Реализуем view для поиска фильма по жанру
@app.route("/genre/<genre>")
def movies_by_genre(genre):
    movies_by_genre = search_movies_by_genre(genre)
    return jsonify(movies_by_genre)


app.run(debug=True, host='0.0.0.0', port=8000)
