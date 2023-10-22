from app.models import Movie, MovieReview
from django.contrib.auth.models import User
from django.shortcuts import render
import sys
import pandas as pd
import math
import os


# This code was based on this tutorial: https://unipython.com/como-desarrollar-un-sistema-de-recomendacion-en-python/


def getRecommendations(request):
    try:
        if not request.user.is_authenticated:
            return render(request, "movies.html", {"movies": Movie.objects.all()})

        moviesReviewed = pd.DataFrame(
            list(
                MovieReview.objects.filter(user=request.user).values(
                    "rating",
                    "movie__title",
                    "movie_id",
                )
            )
        ).rename(columns={"movie__title": "title"})

        if moviesReviewed.empty:
            return render(request, "recommendations.html", {"movies": []})

        movies_df = pd.DataFrame(
            list(
                Movie.objects.all().values(
                    "id",
                    "title",
                )
            )
        ).rename(columns={"id": "movie_id"})

        ratings_df = pd.DataFrame(
            list(
                MovieReview.objects.all().values(
                    "movie_id",
                    "rating",
                    "user_id",
                )
            )
        )

        userSubset = ratings_df[
            ratings_df["movie_id"].isin(moviesReviewed["movie_id"].tolist())
        ]
        print(userSubset.head())
        userSubsetGroup = userSubset.groupby(["user_id"])
        userSubsetGroup = sorted(userSubsetGroup, key=lambda x: len(x[1]), reverse=True)

        userSubsetGroup = userSubsetGroup[0:100]
        pearsonCorrelationDict = {}

        for name, group in userSubsetGroup:
            group = group.sort_values(by="movie_id")
            moviesReviewed = moviesReviewed.sort_values(by="movie_id")

            temp_df = moviesReviewed[
                moviesReviewed["movie_id"].isin(group["movie_id"].tolist())
            ]

            tempRatingList = temp_df["rating"].tolist()
            tempGroupList = group["rating"].tolist()

            data_corr = {
                "tempGroupList": tempGroupList,
                "tempRatingList": tempRatingList,
            }

            print(data_corr)

            pd_corr = pd.DataFrame(data_corr)
            r = pd_corr.corr(method="pearson")["tempRatingList"]["tempGroupList"]

            if math.isnan(r):
                r = 0
            pearsonCorrelationDict[name] = r

        pearsonDf = pd.DataFrame.from_dict(pearsonCorrelationDict, orient="index")
        pearsonDf.columns = ["similarityIndex"]
        pearsonDf["user_id"] = pearsonDf.index
        pearsonDf.index = range(len(pearsonDf))

        return render(request, "recommendations.html", {"movies": moviesReviewed})
    except Exception as e:
        print(f"Error: {e}, line: {sys.exc_info()[-1].tb_lineno}")

        message = "Error while loading recommendations"

        if os.environ.get("DEBUG") == "True":
            message = e

        return render(request, "404.html", {"message": message})
