from app.models import *
from django.shortcuts import render
import json
from app.utils import fetchTMDBApi
from app.forms import MovieReviewForm


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

        movieReviews = MovieReview.objects.filter(movie=movie)
        return render(
            request,
            "movie.html",
            {
                "movie": movie,
                "genres": genres,
                "movieCredits": movieCredits,
                "reviews": movieReviews,
                "form": MovieReviewForm(),
            },
        )

    except Movie.DoesNotExist:
        return render(request, "404.html", {"message": "Movie not found."})
