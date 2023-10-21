from app.models import Person
from django.shortcuts import render
import json
from app.utils import fetchTMDBApi


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
