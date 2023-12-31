# Generated by Django 5.0 on 2023-12-31 11:20

import django.core.validators
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Staff",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "current_status",
                    models.CharField(
                        choices=[("active", "Active"), ("inactive", "Inactive")],
                        default="active",
                        max_length=10,
                    ),
                ),
                (
                    "staff_role",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("Administrative staff", "Administrative staff"),
                            ("Acadamic Staff", "Acadamic Staff"),
                        ],
                        max_length=1024,
                        verbose_name="Staff Role",
                    ),
                ),
                ("name", models.CharField(max_length=200)),
                (
                    "gender",
                    models.CharField(
                        choices=[("male", "Male"), ("female", "Female")],
                        default="male",
                        max_length=10,
                    ),
                ),
                ("date_of_birth", models.DateField(default=django.utils.timezone.now)),
                (
                    "date_of_admission",
                    models.DateField(default=django.utils.timezone.now),
                ),
                (
                    "quali",
                    models.CharField(
                        blank=True,
                        max_length=500,
                        null=True,
                        verbose_name="Qualification",
                    ),
                ),
                (
                    "study_year",
                    models.IntegerField(
                        blank=True,
                        default=None,
                        null=True,
                        verbose_name="If undergoing Year",
                    ),
                ),
                (
                    "study_colleg",
                    models.CharField(
                        blank=True, max_length=1024, verbose_name="College Name"
                    ),
                ),
                (
                    "religion",
                    models.CharField(
                        choices=[
                            ("Hindu", "Hindu"),
                            ("Christian", "Christian"),
                            ("Muslim", "Muslim"),
                            ("others", "others"),
                        ],
                        default="Hindu",
                        max_length=554,
                        verbose_name="Religion",
                    ),
                ),
                (
                    "community",
                    models.CharField(
                        choices=[
                            ("OC", "OC"),
                            ("BC", "BC"),
                            ("MBC", "MBC"),
                            ("ST/SC", "ST/SC"),
                            ("others", "others"),
                        ],
                        default="OC",
                        max_length=524,
                        verbose_name="Community",
                    ),
                ),
                (
                    "software_pro",
                    models.CharField(
                        blank=True, max_length=255, verbose_name="Software Proficiency"
                    ),
                ),
                (
                    "last_salary",
                    models.CharField(
                        blank=True, max_length=255, verbose_name="Last Job Salary drawn"
                    ),
                ),
                (
                    "working_exp",
                    models.TextField(
                        blank=True, null=True, verbose_name="Working Experience"
                    ),
                ),
                (
                    "mobile_number",
                    models.CharField(
                        blank=True,
                        max_length=13,
                        validators=[
                            django.core.validators.RegexValidator(
                                message="Entered mobile number isn't in a right format!",
                                regex="^[0-9]{10,15}$",
                            )
                        ],
                    ),
                ),
                (
                    "email",
                    models.EmailField(default="", max_length=254, verbose_name="Email"),
                ),
                ("address", models.TextField(blank=True)),
                (
                    "passport",
                    models.ImageField(
                        blank=True,
                        upload_to="staff/certificates/",
                        verbose_name="Photo",
                    ),
                ),
                (
                    "aadhar_card",
                    models.ImageField(
                        blank=True,
                        upload_to="staff/certificates/",
                        verbose_name="Aadhar Card",
                    ),
                ),
                (
                    "degree_certificate",
                    models.ImageField(
                        blank=True,
                        upload_to="staff/certificates/",
                        verbose_name="Degree Certificate",
                    ),
                ),
                (
                    "resume",
                    models.ImageField(
                        blank=True,
                        upload_to="staff/certificates/",
                        verbose_name="Resume",
                    ),
                ),
            ],
        ),
    ]