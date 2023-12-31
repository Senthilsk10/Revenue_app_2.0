from django.core.validators import RegexValidator
from datetime import datetime 
from django.db import models
from django.urls import reverse
from django.utils import timezone
from apps.course.models import CourseModel
from apps.staffs.models import Staff
from apps.corecode.models import User
from apps.corecode.models import StudentClass

from ..enquiry.models import *


class Student(models.Model):
    GENDER_CHOICES = [("male", "Male"), ("female", "Female"),("others","others")]
    RELIGION_CHOICE = [('Hindu','Hindu'),('Christian','Christian'),('Muslim','Muslim'),("others","others")]
    COMMUNITY_CHOICE = [('OC','OC'),('BC','BC'),('MBC','MBC'),('ST/SC','ST/SC'),("others","others")]
    STUDENT_ROLE_CHOICES = [
        ("Employed", "Employed"),
        ("Unemployed", "Unemployed"),
        ("Housewife", "Housewife"),
        ("Businessman", "Businessman"),
        ("Student", "Student"),
        ("Others", "Others"),
    ]
    STATUS_CHOICES = [("active", "Active"), ("inactive", "Inactive")]
    if_enq = models.ForeignKey(Enquiry,on_delete=models.PROTECT,default=None,null=True)
    current_status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default="active"
    )
    student_name = models.CharField("Student Name", max_length=255, blank=False, default="")
    enrol_no = models.IntegerField("Enrollment Number",default=0,null=False,unique=True)
    rel_name = models.CharField(
                default=None, max_length=255, verbose_name="Father/Husband Name"
            )
    rel_occupation = models.CharField("Father/Husband Occupation",max_length=255,default=None,null=False)
    date_of_birth = models.DateField(
                default=timezone.now, verbose_name="Date of Birth"
            )
    age = models.IntegerField("Age",default=0,blank=True)
    gender = models.CharField("Gender", max_length=10, choices=GENDER_CHOICES, default="male")
    
    religion = models.CharField("Religion",max_length=554,default="Hindu",choices=RELIGION_CHOICE)
    community = models.CharField("Community",max_length=524,default="OC", choices=COMMUNITY_CHOICE)
    occupation = models.CharField(
                choices=[
                    ("Employed", "Employed"),
                    ("Unemployed", "Unemployed"),
                    ("Housewife", "Housewife"),
                    ("Businessman", "Businessman"),
                    ("Student", "Student"),
                    ("Others", "Others"),
                ],
                default="Student",
                max_length=1024,
                verbose_name="Student Occupation",
            )
    student_company_name = models.CharField(
                blank=True,
                max_length=1024,
                null=True,
                verbose_name="If Emloyed Company Name",
            )
    
    aadhar_no = models.BigIntegerField("Aadhar Number",null=True,default=None,blank=True)

    mobile_num_regex = RegexValidator(
        regex="^[0-9]{10,15}$", message="Entered mobile number isn't in a right format!"
    )
    mobile_number = models.CharField("Mobile Number",
        validators=[mobile_num_regex], max_length=13, blank=True
    )
    email = models.EmailField("Email", blank=False, default="")
 
    #personal Details


    
    passport = models.ImageField("Photo",blank=True, upload_to="students/passports/")
    address = models.CharField("Address", max_length=255,default=None,blank=True)
    address1 = models.CharField("Address Line 2", max_length=255,default=None,blank=True,null=True)
    address2 = models.CharField("Address Line 3", max_length=255,default=None,blank=True,null=True)
    taluka = models.CharField("Taluk",max_length=255,default=None,blank=True,null=True)
    district = models.CharField("District",max_length=255,default=None,blank=True,null=True)
    pincode = models.IntegerField("Pincode", blank=True, default=None)

    #course
    date_of_admission = models.DateField(default=timezone.now)
    course = models.ForeignKey(CourseModel,on_delete=models.PROTECT)
    class_time = models.CharField("Class Timinig",default="2pm - 4pm",max_length=255,null=False)
     

    #fees

    total_fee = models.IntegerField("Total Fees",null=False,default=0)
    remark = models.CharField("Remark",max_length=500,default=None,blank=True)
    
    last_updated = models.DateTimeField(auto_now=True)
    class Meta:
        ordering = ["enrol_no"]

    def __str__(self):
        return f"{self.student_name}({self.enrol_no})"

    def get_absolute_url(self):
        return reverse("student-detail", kwargs={"pk": self.pk})


    def save(self, *args, **kwargs):
        try:
            student_user_instance = User.objects.get(username=self.username)
            created = False
        except User.DoesNotExist:
            student_user_instance = User.objects.create(
                username=self.username,
                password=self.password,  # Set a default password or generate one
                current_status=self.current_status,
                registration_number=self.registration_number,
                surname=self.surname,
                firstname=self.firstname,
                other_name=self.other_name,
                gender=self.gender,
                date_of_birth=self.date_of_birth,
                current_class=self.current_class,
                date_of_admission=self.date_of_admission,
                parent_mobile_number=self.parent_mobile_number,
                address=self.address,
                others=self.others,
                passport=self.passport,
            )
            created = True

        student_user_instance.username = self.username
        student_user_instance.set_password(self.password)  # Set a default password or generate one
        student_user_instance.current_status = self.current_status
        student_user_instance.surname = self.surname
        student_user_instance.firstname = self.firstname
        student_user_instance.other_name = self.other_name
        student_user_instance.gender = self.gender
        student_user_instance.date_of_birth = self.date_of_birth
        student_user_instance.current_class = self.current_class
        student_user_instance.date_of_admission = self.date_of_admission
        student_user_instance.parent_mobile_number = self.parent_mobile_number
        student_user_instance.address = self.address
        student_user_instance.others = self.others
        student_user_instance.passport = self.passport
        student_user_instance.save()

        self.user = student_user_instance
        super().save(*args, **kwargs)

        def delete(self, *args, **kwargs):
        
            try:
                student_user_instance = User.objects.get(id=self.id)
                student_user_instance.delete()
            except Student.DoesNotExist:
                pass 

            super().delete(*args, **kwargs)
    
    
class Bookmodel(models.Model):
    student = models.ForeignKey(Student,on_delete=models.PROTECT)
    received_book = models.CharField("Received Book",max_length=2046,blank=True,default=None)
    received_date = models.DateField("Book received Date",default=timezone.now)
    handled_by = models.ForeignKey(Staff,verbose_name="Handled Staff",on_delete = models.DO_NOTHING)
    def get_absolute_url(self):
        return reverse("student-detail", kwargs={"pk": self.student.pk})
    remark = models.CharField("Remark",max_length=2046,blank=True,default=None)
    last_updated = models.DateTimeField(auto_now=True)
class Classmodel(models.Model):
    student = models.ForeignKey(Student,on_delete=models.PROTECT,blank=True)
    finised_subject = models.CharField("Finised Subject",max_length=255,default=None,blank=False)
    start_date = models.DateField("Started on")
    end_date = models.DateField("Ended on")
    class_time = models.CharField("Class Time",max_length=255,blank=True,null=True,default=None)
    faculty = models.ForeignKey(Staff,verbose_name="Handled Staff",on_delete = models.DO_NOTHING)
    remark = models.CharField("Remark",max_length=2046,blank=True,default=None)
    last_updated = models.DateTimeField(auto_now=True)
    def get_absolute_url(self):
        return reverse("student-detail", kwargs={"pk": self.student.pk})

    
class Exammodel(models.Model):
    student = models.ForeignKey(Student,on_delete=models.PROTECT)
    subject = models.CharField("Subject",max_length=355,default=None,blank=True)
    exam_date = models.DateField("Examed date",default=timezone.now)
    contected_mode = models.CharField("Contected mode",choices=[("Online","Online"),("Offline","Offline")],max_length=255,blank=True,null=True,default=None)
    theory_mark =models.FloatField("Theory mark",blank=True,null=True,default=None)
    paratical_mark = models.FloatField("Paratical mark",blank=True,default=None)
    mark = models.FloatField("Total mark",blank=True)
    remark = models.CharField("Remark",max_length=2046,blank=True,default=None)
    last_updated = models.DateTimeField(auto_now=True)
    def get_absolute_url(self):
        return reverse("student-detail", kwargs={"pk": self.student.pk})

class Certificatemodel(models.Model):
    student = models.ForeignKey(Student,on_delete=models.PROTECT)
    course = models.CharField("Course",max_length=255,blank=True,default=None)
    date_of_complete = models.DateField("Date of Completion",default=timezone.now)
    certificate_no = models.IntegerField("Certificate Number",default=None,blank=True)
    certificate_date = models.DateField("Certificate Date",default=timezone.now)
    certificate_issued_date = models.DateField("Certificate Issued Date",default=timezone.now)
    grade = models.CharField("Grade on Certificate",max_length=10,blank=True,default=None)
    issued_by = models.ForeignKey(Staff,verbose_name ="Certificate Issued By",on_delete = models.DO_NOTHING)
    remark = models.CharField("Remark",max_length=2046,blank=True,default=None)
    last_updated = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return reverse("student-detail", kwargs={"pk": self.student.pk})

    
    
    
    
    
    
    
    
    
    
    
    
    """ 
    STATUS_CHOICES = [("active", "Active"), ("inactive", "Inactive")]

    GENDER_CHOICES = [("male", "Male"), ("female", "Female")]

    current_status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default="active"
    )
    registration_number = models.CharField(max_length=200, unique=True)
    surname = models.CharField(max_length=200)
    firstname = models.CharField(max_length=200)
    other_name = models.CharField(max_length=200, blank=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default="male")
    date_of_birth = models.DateField(default=timezone.now)
    current_class = models.ForeignKey(
        StudentClass, on_delete=models.SET_NULL, blank=True, null=True
    )
    date_of_admission = models.DateField(default=timezone.now)

    mobile_num_regex = RegexValidator(
        regex="^[0-9]{10,15}$", message="Entered mobile number isn't in a right format!"
    )
    parent_mobile_number = models.CharField(
        validators=[mobile_num_regex], max_length=13, blank=True
    )

    address = models.TextField(blank=True)
    others = models.TextField(blank=True)
    passport = models.ImageField(blank=True, upload_to="students/passports/")

    class Meta:
        ordering = ["surname", "firstname", "other_name"]

    def __str__(self):
        return f"{self.surname} {self.firstname} {self.other_name} ({self.registration_number})"

    def get_absolute_url(self):
        return reverse("student-detail", kwargs={"pk": self.pk})

 """
class StudentBulkUpload(models.Model):
    date_uploaded = models.DateTimeField(auto_now=True)
    csv_file = models.FileField(upload_to="students/bulkupload/")
