from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from app.models import *
from faker import Faker

fake = Faker()


class Command(BaseCommand):
    help = "Load genres from TMDB API"

    def handle(self, *args, **options):
        users = User.objects.all()

        movies = Movie.objects.all()

        for user in users:
            moviesToReview = movies.order_by("?")[:10]

            rating = fake.random_int(min=1, max=100)
            review = fake.text()

            for movie in moviesToReview:
                MovieReview.objects.create(
                    movie=movie,
                    user=user,
                    rating=rating,
                    review=review,
                )

                print("Review created: " + movie.title + " - " + user.username)
