# Generated by Django 4.2.6 on 2023-10-19 23:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0016_alter_person_birthdate"),
    ]

    operations = [
        migrations.AlterField(
            model_name="person",
            name="birthdate",
            field=models.DateField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name="person",
            name="place_of_birth",
            field=models.CharField(blank=True, default=None, max_length=100),
        ),
        migrations.AlterField(
            model_name="person",
            name="profile_path",
            field=models.URLField(blank=True, default=None, null=True),
        ),
    ]