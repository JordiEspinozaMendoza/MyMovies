# Generated by Django 4.2.6 on 2023-10-07 21:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0002_remove_genre__id_genre_tmbd_id"),
    ]

    operations = [
        migrations.RenameField(
            model_name="genre",
            old_name="tmbd_id",
            new_name="tmdb_id",
        ),
    ]
