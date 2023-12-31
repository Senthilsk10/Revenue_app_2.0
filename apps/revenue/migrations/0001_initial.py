# Generated by Django 5.0 on 2023-12-31 11:20

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="revenue",
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
                ("Total_student", models.IntegerField(default=None)),
                ("Total_paid", models.DecimalField(decimal_places=2, max_digits=10)),
                ("Total_Income", models.DecimalField(decimal_places=2, max_digits=10)),
                ("Total_Balance", models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
    ]