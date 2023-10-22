from django.contrib import admin
from django.urls import path
from app.views import movie, movieReview, person, auth, recommendations
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/login/", auth.CustomLoginView.as_view(), name="login"),
    path("accounts/logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("accounts/signup/", auth.CustomSignUpView, name="logout"),
    path("", movie.getMoviesList, name="home"),
    path("movies/<int:id>", movie.getMovieDetails, name="movieDetails"),
    path("people/<int:id>", person.getPersonDetails, name="personDetails"),
    path("movies/", movie.getMoviesList, name="movies"),
    path("submitReview/<int:id>", movieReview.submitReview, name="submitReview"),
    path(
        "recommendations/",
        recommendations.getRecommendations,
        name="recommendations",
    ),
]
