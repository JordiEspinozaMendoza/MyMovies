from app.models import *
from django.shortcuts import render
from app.forms import MovieReviewForm


def submitReview(request, id):
    try:
        movie = Movie.objects.get(tmdb_id=id)
        form = MovieReviewForm(request.POST)

        movieReviews = MovieReview.objects.filter(movie=movie)

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
                    "reviews": movieReviews,
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
                "reviews": movieReviews,
            },
        )

    except Movie.DoesNotExist:
        return render(request, "404.html", {"message": "Movie not found."})
