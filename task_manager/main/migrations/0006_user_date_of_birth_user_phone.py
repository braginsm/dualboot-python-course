# Generated by Django 4.2.1 on 2023-06-08 10:54

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("main", "0005_alter_task_assigned_alter_task_author"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="date_of_birth",
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="user",
            name="phone",
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]