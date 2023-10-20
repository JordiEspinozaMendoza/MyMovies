from django.shortcuts import render
from .models import *
import json
from app.utils import fetchTMDBApi


def getMoviesList(request):
    movies = Movie.objects.all()

    return render(request, "movies.html", {"movies": movies})


def getMovieDetails(request, id):
    try:
        movie = Movie.objects.get(tmdb_id=id)
        genres = movie.genres.all()

        movieCredits = MovieCredit.objects.filter(movie=movie)

        if movieCredits.count() == 0:
            response = fetchTMDBApi("/movie/" + str(id) + "/credits")

            data = json.dumps(response.json()["cast"])

            cast = json.loads(data)

            for person in cast:
                MovieCredit.objects.create(
                    movie=movie,
                    personTMDBId=person["id"],
                    name=person["name"],
                    character=person["character"],
                    profile_path=person["profile_path"],
                    known_for_department=person["known_for_department"],
                )

            movieCredits = MovieCredit.objects.filter(movie=movie)

        return render(
            request,
            "movie.html",
            {"movie": movie, "genres": genres, "movieCredits": movieCredits},
        )

    except Movie.DoesNotExist:
        return render(request, "404.html", {"message": "Movie not found."})


def getPersonDetails(request, id):
    try:
        person = Person.objects.filter(tmdb_id=id).first()

        if person is None:
            response = fetchTMDBApi("/person/" + str(id))

            data = json.loads(json.dumps(response.json()))

            if "success" in data and data["success"] == False:
                return render(request, "404.html", {"message": "Person not found."})

            Person.objects.create(
                name=data["name"],
                birthdate=data["birthday"],
                place_of_birth=data["place_of_birth"],
                profile_path=data["profile_path"],
                known_for_department=data["known_for_department"],
                tmdb_id=data["id"],
            )

            createdPerson = Person.objects.filter(tmdb_id=id).first()

            return render(
                request,
                "person.html",
                {"person": createdPerson},
            )

        return render(
            request,
            "person.html",
            {"person": person},
        )

    except Exception as e:
        print(e)
        return render(request, "404.html", {"message": "error"})
