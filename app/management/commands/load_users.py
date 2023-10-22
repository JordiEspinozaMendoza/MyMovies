from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from faker import Faker

fake = Faker()


class Command(BaseCommand):
    help = "Load genres from TMDB API"

    def handle(self, *args, **options):
        for i in range(0, 100):
            user = {
                "first_name": fake.name(),
                "last_name": fake.name(),
                "email": fake.email(),
                "password": fake.password(),
            }

            user = User.objects.create_user(
                username=user["email"],
                email=user["email"],
                password=user["password"],
                first_name=user["first_name"],
                last_name=user["last_name"],
            )

            user.save()

            print("User created: " + user.username)
