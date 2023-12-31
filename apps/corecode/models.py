from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.core.validators import RegexValidator

class SiteConfig(models.Model):
    """Site Configurations"""

    key = models.SlugField()
    value = models.CharField(max_length=200)

    def __str__(self):
        return self.key


class AcademicSession(models.Model):
    """Academic Session"""

    name = models.CharField(max_length=200, unique=True)
    current = models.BooleanField(default=True)

    class Meta:
        ordering = ["-name"]

    def __str__(self):
        return self.name


class AcademicTerm(models.Model):
    """Academic Term"""

    name = models.CharField(max_length=20, unique=True)
    current = models.BooleanField(default=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Subject(models.Model):
    """Subject"""

    name = models.CharField(max_length=200, unique=True)
    duration = models.CharField(max_length=200,blank=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name
class Book(models.Model):
    """Book"""

    name = models.CharField(max_length=200, unique=True,blank=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name
class Exam(models.Model):
    """Exam"""

    name = models.CharField(max_length=200, unique=True,blank=True)
    exam_mode = models.CharField(max_length=255,choices=[("Online","online"),("Offline","Offline")],default="Offline")
    exam_duration = models.CharField(max_length=200,blank=True)


    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class StudentClass(models.Model):
    name = models.CharField(max_length=200, unique=True)

    class Meta:
        verbose_name = "Class"
        verbose_name_plural = "Classes"
        ordering = ["name"]

    def __str__(self):
        return self.name



class User(AbstractUser):
    STATUS = [("active", "Active"), ("inactive", "Inactive")]

    GENDER = [("male", "Male"), ("female", "Female")]

    current_status = models.CharField(max_length=10, choices=STATUS, default="active")
    registration_number = models.CharField(max_length=200)
    surname = models.CharField(max_length=200)
    firstname = models.CharField(max_length=200)
    other_name = models.CharField(max_length=200, blank=True)
    gender = models.CharField(max_length=10, choices=GENDER, default="male")
    date_of_birth = models.DateField(default=timezone.now)
    current_class = models.ForeignKey(
        StudentClass, on_delete=models.SET_NULL, blank=True, null=True
    )
    date_of_admission = models.DateField(default=timezone.now)
    quali = models.CharField("Qualification",blank=True, max_length=500)

    mobile_num_regex = RegexValidator(
        regex="^[0-9]{10,15}$", message="Entered mobile number isn't in a right format!"
    )
    mobile_number = models.CharField(
        validators=[mobile_num_regex], max_length=13, blank=True
    )
    parent_mobile_number = models.CharField(
        validators=[mobile_num_regex], max_length=13, blank=True
    )

    address = models.TextField(blank=True)
    others = models.TextField(blank=True)
    passport = models.ImageField(blank=True, upload_to="students/passports/")
    def __str__(self):
        return f"{self.surname} {self.firstname} {self.other_name}"