# Generated by Django 5.0.4 on 2024-04-21 17:19

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("pages", "0005_catagories"),
    ]

    operations = [
        migrations.CreateModel(
            name="BookLike",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("bookId", models.IntegerField()),
                ("liked", models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name="BookVisited",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("bookId", models.IntegerField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
