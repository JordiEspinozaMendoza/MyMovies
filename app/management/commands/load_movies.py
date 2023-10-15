from django.core.management.base import BaseCommand, CommandError
from app.models import Movie, Genre
import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()


class Command(BaseCommand):
    help = "Load movies from TMDB API"

    def handle(self, *args, **options):
        url = os.environ.get("TMDB_API_URL")

        headers = {
            "accept": "application/json",
            "Authorization": "Bearer " + os.environ.get("TMDB_READ_ACCESS_TOKEN"),
        }

        response = requests.get(url + "/movie/popular", headers=headers)
        movies = json.dumps(response.json()["results"])

        genres = Genre.objects.all()
        try:
            for movie in json.loads(movies):
                genre_ids = movie["genre_ids"]

                movie_genres = []

                for genre in genres:
                    if genre.tmdb_id in genre_ids:
                        movie_genres.append(genre)

                Movie.objects.create(
                    title=movie["title"],
                    release_date=movie["release_date"],
                    overview=movie["overview"],
                    poster_path=movie["poster_path"],
                    tmdb_id=movie["id"],
                ).genres.set(movie_genres)

                print("Movie " + movie["title"] + " loaded")

            print("Movies loaded")

        except Exception as e:
            raise CommandError("Error loading movies: " + str(e))
