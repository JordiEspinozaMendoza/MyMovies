from django.core.management.base import BaseCommand, CommandError
from app.models import Genre
import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()


class Command(BaseCommand):
    help = "Load genres from TMDB API"

    def handle(self, *args, **options):
        url = os.environ.get("TMDB_API_URL")

        headers = {
            "accept": "application/json",
            "Authorization": "Bearer " + os.environ.get("TMDB_READ_ACCESS_TOKEN"),
        }

        response = requests.get(url + "/genre/movie/list", headers=headers)
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
