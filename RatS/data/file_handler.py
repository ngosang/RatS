import json
import os

from RatS.data.movie import Movie

EXPORTS_FOLDER = os.path.abspath(os.path.join(os.path.dirname(__file__), 'RatS', 'exports'))


def load_movies_json(folder=EXPORTS_FOLDER, filename='import.json'):
    with open(os.path.join(folder, filename)) as file:
        movies_json = json.load(file)
        file.close()
        return [Movie.from_json(movie) for movie in movies_json]


def save_movies_json(movies, folder=EXPORTS_FOLDER, filename='export.json'):
    if not os.path.exists(folder):
        os.makedirs(folder)
    with open(os.path.join(folder, filename), 'w+') as file:
        movies_json = [movie.to_json() for movie in movies]
        file.write(json.dumps(movies_json))
        file.close()
