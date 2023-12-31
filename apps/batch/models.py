from django.db import models
from apps.course.models import CourseModel
from apps.staffs.models import Staff
from apps.students.models import Student
from django.utils import timezone
from django.urls import reverse

class BatchModel(models.Model):
    batch_status = models.CharField("Batch Status",max_length=255,choices=[("Active","Active"),("Inactive","Inactive")])
    batch_id = models.CharField("Batch Id",max_length=255,blank=True)
    batch_course = models.ForeignKey(CourseModel,on_delete=models.PROTECT)
    batch_staff = models.ForeignKey(Staff,on_delete=models.PROTECT)
    batch_students = models.ManyToManyField(Student)
    batch_start_date = models.DateField("Batch Start Date",default=timezone.now)
    batch_end_date = models.DateField("Batch End Date",default=timezone.now)
    batch_timing = models.CharField("Batch Timing",max_length=255,blank=True)

    def total_student(self):
        return self.batch_students.count()
    def get_absolute_url(self):
        return reverse("batch_detail", kwargs={"pk": self.pk})
    
    @property
    def is_active(self):
        return self.batch_status == "Active"

    def calculate_duration(self):
        return (self.batch_end_date - self.batch_start_date).days


    class Meta:
        ordering = ["-batch_start_date"]

    
