import requests
import os
from dotenv import load_dotenv

load_dotenv()


def fetchTMDBApi(path):
    try:
        url = os.environ.get("TMDB_API_URL")

        headers = {
            "accept": "application/json",
            "Authorization": "Bearer " + os.environ.get("TMDB_READ_ACCESS_TOKEN"),
        }
        response = requests.get(url + path, headers=headers)

        return response
    except Exception as e:
        raise Exception("Error fetching TMDB API: " + str(e))
