from .models import *
from django.shortcuts import render, redirect
import json
from app.utils import fetchTMDBApi
from django.contrib.auth.views import LoginView
from .forms import CustomLoginForm, MovieReviewForm, CustomSignUpForm
from django.contrib.auth import login


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


def submitReview(request, id):
    try:
        movie = Movie.objects.get(tmdb_id=id)
        form = MovieReviewForm(request.POST)

        if form.is_valid():
            MovieReview.objects.create(
                movie=movie,
                user=request.user,
                rating=form.cleaned_data["rating"],
                review=form.cleaned_data["review"],
            )

            return render(
                request,
                "movie.html",
                {
                    "movie": movie,
                    "genres": movie.genres.all(),
                    "movieCredits": MovieCredit.objects.filter(movie=movie),
                    "form": MovieReviewForm(),
                    "message": "Review submitted successfully.",
                },
            )

        return render(
            request,
            "movie.html",
            {
                "movie": movie,
                "genres": movie.genres.all(),
                "movieCredits": MovieCredit.objects.filter(movie=movie),
                "form": form,
                "message": "Invalid form.",
            },
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
                biography=data["biography"],
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


class CustomLoginView(LoginView):
    form_class = CustomLoginForm
    template_name = "login.html"


def CustomSignUpView(request):
    if request.user.is_authenticated:
        return redirect("/")

    if request.method == "POST":
        form = CustomSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("/")
    else:
        form = CustomSignUpForm()

    return render(request, "sign_up.html", {"form": form})
