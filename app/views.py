from django.shortcuts import render
from .models import *


def getMoviesList(request):
    movies = Movie.objects.all()

    return render(request, "movies.html", {"movies": movies})
