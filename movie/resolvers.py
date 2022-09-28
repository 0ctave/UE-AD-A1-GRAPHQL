import json

from graphql import GraphQLError


def movie_with_id(_, info, _id):
    with open('{}/data/movies.json'.format("."), "r") as file:
        movies = json.load(file)
        for movie in movies['movies']:
            if movie['id'] == _id:
                return movie
        raise GraphQLError('ID not found')


def movie_with_title(_, info, _title):
    with open('{}/data/movies.json'.format("."), "r") as file:
        movies = json.load(file)
        for movie in movies['movies']:
            if movie['title'] == _title:
                return movie
        raise GraphQLError('title not found')


def movie_with_director(_, info, _director):
    with open('{}/data/movies.json'.format("."), "r") as file:
        movies = json.load(file)
        for movie in movies['movies']:
            if movie['director'] == _director:
                return movie
        raise GraphQLError('director not found')


def create_movie(_, info, _id, _title, _rating, _director):
    with open('{}/data/movies.json'.format("."), "r+") as file:
        movies = json.load(file)
        for movie in movies['movies']:
            if movie["id"] == _id:
                raise GraphQLError('movie ID already exists')
        movie = {"id": _id, "director": _director, "title": _title, "rating": _rating}
        file.seek(0)
        file.truncate()
        movies['movies'].append(movie)
        json.dump(movies, file,
                  indent=4,
                  separators=(',', ': '))
        return movie


def update_movie_rating_with_id(_, info, _id, _rating):
    with open('{}/data/movies.json'.format("."), "r+") as file:
        movies = json.load(file)
        for movie in movies['movies']:
            if movie["id"] == _id:
                movie["rating"] = _rating
                file.seek(0)
                json.dump(movies, file,
                          indent=4,
                          separators=(',', ': '))
                file.truncate()
                return movie
        raise GraphQLError('ID not found')


def del_movie_with_id(_, info, _id):
    with open('{}/data/movies.json'.format("."), "r+") as file:
        movies = json.load(file)
        for movie in movies['movies']:
            if movie["id"] == _id:
                movies['movies'].remove(movie)
                file.seek(0)
                json.dump(movies, file,
                          indent=4,
                          separators=(',', ': '))
                file.truncate()
                return movie
        raise GraphQLError('ID not found')


def movies_rate_above_rating(_, info, _rating):
    with open('{}/data/movies.json'.format("."), "r") as file:
        movies = json.load(file)
        movie_list = []
        for movie in movies['movies']:
            if float(movie["rating"]) >= _rating:
                movie_list.append(movie)
        return movie_list
