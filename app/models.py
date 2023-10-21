from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator


class Studio(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Genre(models.Model):
    tmdb_id = models.IntegerField(blank=True, unique=True, default=None)

    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Job(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Person(models.Model):
    name = models.CharField(max_length=100)
    birthdate = models.DateField(blank=True, null=True, default=None)
    place_of_birth = models.CharField(
        max_length=100, blank=True, default=None, null=True
    )
    profile_path = models.URLField(blank=True, default=None, null=True)
    known_for_department = models.CharField(max_length=100, blank=True)
    tmdb_id = models.IntegerField(blank=True, unique=True, default=None)
    biography = models.TextField(blank=True, default=None, null=True)

    def __str__(self):
        return self.name


class Movie(models.Model):
    title = models.CharField(max_length=100)
    release_date = models.DateTimeField()
    overview = models.TextField(blank=True)
    poster_path = models.URLField()
    studio = models.ForeignKey(Studio, on_delete=models.CASCADE, null=True)
    genres = models.ManyToManyField(Genre)
    tmdb_id = models.IntegerField(blank=True, unique=True)
    credits = models.ManyToManyField(Person, through="MovieCredit")

    def __str__(self):
        return self.title


class MovieCredit(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    person = models.ForeignKey(Person, on_delete=models.CASCADE, null=True)
    personTMDBId = models.IntegerField(blank=True, default=None)
    name = models.CharField(max_length=100, blank=True)
    character = models.CharField(max_length=100, blank=True)
    profile_path = models.URLField(blank=True, default=None, null=True)
    known_for_department = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.name


class MovieReview(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(100)]
    )
    review = models.TextField(blank=True)
