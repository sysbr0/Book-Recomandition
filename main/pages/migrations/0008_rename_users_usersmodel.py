# Generated by Django 5.0.4 on 2024-05-14 23:45

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("pages", "0007_agee_getvisited_users"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="users",
            new_name="UsersModel",
        ),
    ]
