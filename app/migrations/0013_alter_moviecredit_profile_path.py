# Generated by Django 4.2.6 on 2023-10-19 23:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0012_alter_moviecredit_profile_path"),
    ]

    operations = [
        migrations.AlterField(
            model_name="moviecredit",
            name="profile_path",
            field=models.URLField(blank=True, default=None, null=True),
        ),
    ]
