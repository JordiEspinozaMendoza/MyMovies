from django.core.management.base import BaseCommand, CommandError
from app.models import Job
import json
from app.utils import fetchTMDBApi


class Command(BaseCommand):
    help = "Load jobd from TMDB API"

    def handle(self, *args, **options):
        response = fetchTMDBApi("/configuration/jobs")

        jobs = json.dumps(response.json())

        try:
            for job in json.loads(jobs):
                for jobName in job["jobs"]:
                    Job.objects.create(
                        name=jobName,
                    )

                    print("Job " + jobName + " loaded")

            print("Jobs loaded")

        except Exception as e:
            raise CommandError("Error loading jobs: " + str(e))
