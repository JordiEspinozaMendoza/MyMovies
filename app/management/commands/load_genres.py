from django.core.management.base import BaseCommand, CommandError
from app.models import Genre
from app.utils import fetchTMDBApi
import json


class Command(BaseCommand):
    help = "Load genres from TMDB API"

    def handle(self, *args, **options):
        response = fetchTMDBApi("/genre/movie/list")

        genres = json.dumps(response.json()["genres"])

        try:
            for genre in json.loads(genres):
                Genre.objects.create(
                    name=genre["name"],
                    tmdb_id=genre["id"],
                )

                print("Genre " + genre["name"] + " loaded")

            print("Genres loaded")

        except Exception as e:
            raise CommandError("Error loading genres: " + str(e))
