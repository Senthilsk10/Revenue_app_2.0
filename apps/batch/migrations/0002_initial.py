# Generated by Django 5.0 on 2023-12-31 11:20

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("batch", "0001_initial"),
        ("course", "0001_initial"),
        ("staffs", "0001_initial"),
        ("students", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="batchmodel",
            name="batch_course",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT, to="course.coursemodel"
            ),
        ),
        migrations.AddField(
            model_name="batchmodel",
            name="batch_staff",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT, to="staffs.staff"
            ),
        ),
        migrations.AddField(
            model_name="batchmodel",
            name="batch_students",
            field=models.ManyToManyField(to="students.student"),
        ),
    ]
