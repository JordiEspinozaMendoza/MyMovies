from app.models import Movie, MovieReview
from django.shortcuts import render
import sys
import pandas as pd
from math import sqrt
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
        userSubsetGroup = userSubset.groupby(["user_id"])
        userSubsetGroup = sorted(userSubsetGroup, key=lambda x: len(x[1]), reverse=True)

        userSubsetGroup = userSubsetGroup[0:100]
        pearsonCorrelationDict = {}

        for name, group in userSubsetGroup:
            group = group.sort_values(by="movie_id")
            moviesReviewed = moviesReviewed.sort_values(by="movie_id")
            nRatings = len(group)
            temp_df = moviesReviewed[
                moviesReviewed["movie_id"].isin(group["movie_id"].tolist())
            ]

            tempRatingList = temp_df["rating"].tolist()
            tempGroupList = group["rating"].tolist()

            Sxx = sum([i**2 for i in tempRatingList]) - pow(
                sum(tempRatingList), 2
            ) / float(nRatings)
            Syy = sum([i**2 for i in tempGroupList]) - pow(
                sum(tempGroupList), 2
            ) / float(nRatings)
            Sxy = sum(i * j for i, j in zip(tempRatingList, tempGroupList)) - sum(
                tempRatingList
            ) * sum(tempGroupList) / float(nRatings)

            if Sxx != 0 and Syy != 0:
                pearsonCorrelationDict[name] = Sxy / sqrt(Sxx * Syy)
            else:
                pearsonCorrelationDict[name] = 0

        pearsonDf = pd.DataFrame.from_dict(pearsonCorrelationDict, orient="index")
        pearsonDf.columns = ["similarityIndex"]
        pearsonDf.index = (
            pearsonDf.index.map(str)
            .map(lambda x: x.replace("(", ""))
            .map(lambda x: x.replace(",)", ""))
        )
        pearsonDf["user_id"] = pearsonDf.index
        pearsonDf["user_id"] = pearsonDf["user_id"].astype(int)
        pearsonDf.index = range(len(pearsonDf))

        topUsers = pearsonDf.sort_values(by="similarityIndex", ascending=False)[0:50]
        topUsersRating = topUsers.merge(
            ratings_df, left_on="user_id", right_on="user_id", how="inner"
        )
        topUsersRating["weightedRating"] = (
            topUsersRating["similarityIndex"] * topUsersRating["rating"]
        )
        tempTopUsersRating = topUsersRating.groupby("movie_id").sum()[
            ["similarityIndex", "weightedRating"]
        ]
        tempTopUsersRating.columns = ["sum_similarityIndex", "sum_weightedRating"]

        recommendation_df = pd.DataFrame()
        recommendation_df["weighted average recommendation score"] = (
            tempTopUsersRating["sum_weightedRating"]
            / tempTopUsersRating["sum_similarityIndex"]
        )
        recommendation_df["movie_id"] = tempTopUsersRating.index

        recommendation_df = recommendation_df.sort_values(
            by="weighted average recommendation score", ascending=False
        )[0:10]

        movies = Movie.objects.filter(id__in=recommendation_df["movie_id"].tolist())

        return render(request, "recommendations.html", {"movies": movies})
    except Exception as e:
        print(f"Error: {e}, line: {sys.exc_info()[-1].tb_lineno}")

        message = "Error while loading recommendations"

        if os.environ.get("DEBUG") == "True":
            message = e

        return render(request, "404.html", {"message": message})
