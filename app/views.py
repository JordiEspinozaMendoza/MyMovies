from django.shortcuts import render
from .models import *


def getMoviesList(request):
    movies = Movie.objects.all()

    return render(request, "movies.html", {"movies": movies})


def getMovieDetails(request, id):
    try:
        movie = Movie.objects.get(tmdb_id=id)

        return render(request, "movie.html", {"movie": movie})

    except Movie.DoesNotExist:
        return render(request, "404.html", {"message": "Movie not found."})
