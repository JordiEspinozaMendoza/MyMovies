# Generated by Django 4.2.6 on 2023-10-19 22:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0009_remove_moviecredit_role_moviecredit_job"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="moviecredit",
            name="job",
        ),
        migrations.AddField(
            model_name="moviecredit",
            name="known_for_department",
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
