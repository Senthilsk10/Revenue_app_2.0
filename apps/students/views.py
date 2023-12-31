import csv
from django.contrib.auth.mixins import AccessMixin
from datetime import datetime
from django import forms
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.forms import widgets
from django.http import HttpResponse,Http404
from django.shortcuts import redirect, render,get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView, View
from django.views.generic.edit import FormMixin, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import (
    CreateView,
    DeleteView,
    FormMixin,
    UpdateView,
)
from ..finance.models import Invoice,InvoiceItem
from django.views.generic import DetailView

from apps.finance.models import Invoice

from ..enquiry.models import *
from .models import Student, StudentBulkUpload,Bookmodel,Classmodel,Exammodel,Certificatemodel

def handler404(request, exception):
    return render(request, '404.html', status=404)

class StudentListView(LoginRequiredMixin, ListView):
    model = Student
    
    def slist(request):
        template_name = "students/student_list.html"
        return render(request, template_name , context={"students":Student.objects.all()})

def select_enquiry(request):
    enquiries = Enquiry.objects.filter(enquiry_status = "Following")
    if request.method == 'POST':
        selected_enquiry_id = request.POST.get('enquiry')
        # Redirect to the next page with the selected Enquiry ID
        return redirect('student-create', enquiry_id=selected_enquiry_id)

    return render(request, 'students/ad_con.html', {'enquiries': enquiries})

class StudentDetailView(LoginRequiredMixin, DetailView):
    model = Student
    template_name = "students/student_detail.html"

    def get_context_data(self, **kwargs):
        context = super(StudentDetailView, self).get_context_data(**kwargs)
        context["payments"] = Invoice.objects.filter(student=self.object)
        context["booklog"] = Bookmodel.objects.filter(student=self.object)
        context["classlog"] = Classmodel.objects.filter(student=self.object)
        context["examlog"] = Exammodel.objects.filter(student=self.object)
        context["certilog"] = Certificatemodel.objects.filter(student=self.object)
        return context


class StudentCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Student
    fields = "__all__"
    success_message = "New student successfully added."
    def automatic_ro(self):
            id = Student.objects.count()
            year = str(datetime.now().year)[-2:]  # Last two digits of the current year
            month = str(datetime.now().month).zfill(2)  # Month with leading zero if needed
            object_id = str(id).zfill(4)  # Object ID with leading zeros if needed
            return f'{year}{month}{object_id}'
    def get(self, request, *args, **kwargs):
        # Stage 1: Select Enquiry
        if 'enquiry_id' not in kwargs:
            enquiries = Enquiry.objects.all()
            return render(request, 'students/ad_con.html', {'enquiries': enquiries})

        # Stage 2: Add Student Information
        enquiry_id = kwargs['enquiry_id']
        enquiry = Enquiry.objects.get(auto_increment=enquiry_id)
       
        
        

        # Create a dynamic ModelForm for the Student model
        class StudentForm(forms.ModelForm):
            
            class Meta:
                model = Student
                fields = '__all__'
                def __init__(self, *args, **kwargs):
                    super().__init__(*args, **kwargs)
                    # Make the 'enquiry_id' field readonly
                    


        form = StudentForm()
        form.initial['if_enq'] = enquiry_id
        form.fields['if_enq'].widget = forms.HiddenInput()
        form.fields['if_enq'].label = ""
        enquiry_id = enquiry_id  # self.kwargs.get('if_enq')

        try:
            # If enquiry_id is provided, fetch the Enquiry instance
            if enquiry_id:
                enquiry_instance = Enquiry.objects.get(pk=enquiry_id)
                
                # Pre-fill the form fields based on the Enquiry instance
                form.initial['student_name'] = enquiry_instance.name
                form.initial['enrol_no'] = self.automatic_ro()
                form.initial['date_of_birth'] = enquiry_instance.date_of_birth
                form.initial['address'] = enquiry_instance.address
                form.initial['address1'] = enquiry_instance.address1
                form.initial['address2'] = enquiry_instance.address2
                form.initial['rel_name'] = enquiry_instance.f_name
                form.initial['date_of_birth'] = enquiry_instance.date_of_birth
                form.initial['age'] = enquiry_instance.age
                form.initial['gender'] = enquiry_instance.gender
                form.initial['occupation'] = enquiry_instance.student_role
                form.initial['mobile_number'] = enquiry_instance.mobile_number
                form.initial['email'] = enquiry_instance.email
                form.initial['taluka'] = enquiry_instance.taluka
                form.initial['district'] = enquiry_instance.district
                form.initial['pincode'] = enquiry_instance.pincode
                

        except Enquiry.DoesNotExist:
            raise Http404("Enquiry does not exist")

       
        return render(request, 'students/student_form.html', {'form': form, 'enquiry_id': enquiry_id, 'enquiry': enquiry})

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        
        # Retrieve the enquiry_id from the URL parameters
        # Add date pickers and customize widgets
        form.fields["date_of_birth"].widget = widgets.DateInput(attrs={"type": "date"})
        form.fields["date_of_admission"].widget = widgets.DateInput(attrs={"type": "date"})
        form.fields["address"].widget = widgets.Textarea(attrs={"rows": 2})

        return form
    
    def post(self, request, *args, **kwargs):
            # Stage 2: Add Student Information
            enquiry_id = kwargs['enquiry_id']
            enquiry = Enquiry.objects.get(auto_increment=enquiry_id)
            self.usefrfollow =enquiry_id

            # Create a dynamic ModelForm for the Student model
            class StudentForm(forms.ModelForm):
                class Meta:
                    model = Student
                    fields = '__all__'

            form = StudentForm(request.POST,request.FILES)
            
            if form.is_valid():
                if 'passport' in request.FILES:
                    form.cleaned_data['passport'] = request.FILES['passport']
                return self.form_valid(form)
            


            return render(request, self.template_name, {'form': form, 'enquiry_id': enquiry_id, 'enquiry': enquiry})

    def form_valid(self, form):
            # Additional logic after the form is valid
            response = super().form_valid(form)
            total_fee = form.cleaned_data.get('total_fee', 0)
            invoice = Invoice.objects.create(
            student=self.object, 
            status = "Active",)
            invoice_create = InvoiceItem.objects.create(
            invoice = invoice,
            description = "Total Fee",
            amount = total_fee
            )
            objectcha = Enquiry.objects.filter(auto_increment=self.usefrfollow)
            for object1 in objectcha:
                object1.enquiry_status = "Admitted"
                object1.save()
            return response
    
def Studentdashboard(request):
    return render(request,"students/student_dashboard.html")

class StudentUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Student
    fields = "__all__"
    success_message = "Record successfully updated."

    def get_form(self):
        """add date picker in forms"""
        form = super(StudentUpdateView, self).get_form()
        form.fields["date_of_birth"].widget = widgets.DateInput(attrs={"type": "date"})
        form.fields["date_of_admission"].widget = widgets.DateInput(
            attrs={"type": "date"}
        )
        form.fields["address"].widget = widgets.Textarea(attrs={"rows": 2})
      
        return form


class StudentDeleteView(LoginRequiredMixin, DeleteView):
    model = Student
    success_url = reverse_lazy("student-list")


class StudentBulkUploadView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = StudentBulkUpload
    template_name = "students/students_upload.html"
    fields = ["csv_file"]
    success_url = "/student/list"
    success_message = "Successfully uploaded students"


class DownloadCSVViewdownloadcsv(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="student_template.csv"'

        writer = csv.writer(response)
        writer.writerow(
            [
                "registration_number",
                "surname",
                "firstname",
                "other_names",
                "gender",
                "parent_number",
                "address",
                "current_class",
            ]
        )

        return response

class CreateBooklLog(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Bookmodel
    fields = '__all__'
    template_name = "books/add_logs.html"
    def get(self, request, *args, **kwargs):
        class BookForm(forms.ModelForm):
                class Meta:
                    model = Bookmodel
                    fields = '__all__'
        form = BookForm()
        if "pk" in kwargs:
            form.initial['student'] = kwargs['pk']
            form.fields['student'].widget = forms.HiddenInput()
            form.fields['student'].label = ""
            form.fields["received_date"].widget = widgets.DateInput(attrs={"type": "date"})
            
        return render(request, 'books/add_logs.html', {'form': form})
    def post(self, request, *args, **kwargs):

            # Create a dynamic ModelForm for the Student model
            class BookForm(forms.ModelForm):
                class Meta:
                    model = Bookmodel
                    fields = '__all__'

            form = BookForm(request.POST)
            
            if form.is_valid():
                return self.form_valid(form)
            
            return render(request, self.template_name, {'form': form})

    def form_valid(self, form):
            # Additional logic after the form is valid
            response = super().form_valid(form)
            return response
class CreateClasslLog(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Classmodel
    fields = '__all__'
    template_name = "classes/add_class.html"
    def get(self, request, *args, **kwargs):
        class ClassForm(forms.ModelForm):
                class Meta:
                    model = Classmodel
                    fields = '__all__'
        form = ClassForm()
        if "pk" in kwargs:
            form.initial['student'] = kwargs['pk']
            form.fields['student'].widget = forms.HiddenInput()
            form.fields['student'].label = ""
            form.fields["start_date"].widget = widgets.DateInput(attrs={"type": "date"})
            form.fields["end_date"].widget = widgets.DateInput(attrs={"type": "date"})
            
        return render(request, 'classes/add_class.html', {'form': form})
    def post(self, request, *args, **kwargs):

           
            class ClassForm(forms.ModelForm):
                class Meta:
                    model = Classmodel
                    fields = '__all__'

            form = ClassForm(request.POST)
            
            if form.is_valid():
                return self.form_valid(form)
            
            return render(request, self.template_name, {'form': form})

    def form_valid(self, form):
            # Additional logic after the form is valid
            response = super().form_valid(form)
            return response
class CreateClasslLog(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Classmodel
    fields = '__all__'
    template_name = "classes/add_class.html"
    def get(self, request, *args, **kwargs):
        class ClassForm(forms.ModelForm):
                class Meta:
                    model = Classmodel
                    fields = '__all__'
        form = ClassForm()
        if "pk" in kwargs:
            form.initial['student'] = kwargs['pk']
            form.fields['student'].widget = forms.HiddenInput()
            form.fields['student'].label = ""
            form.fields["start_date"].widget = widgets.DateInput(attrs={"type": "date"})
            form.fields["end_date"].widget = widgets.DateInput(attrs={"type": "date"})
            
        return render(request, 'classes/add_class.html', {'form': form})
    def post(self, request, *args, **kwargs):

           
            class ClassForm(forms.ModelForm):
                class Meta:
                    model = Classmodel
                    fields = '__all__'

            form = ClassForm(request.POST)
            
            if form.is_valid():
                return self.form_valid(form)
            
            return render(request, self.template_name, {'form': form})

    def form_valid(self, form):
            # Additional logic after the form is valid
            response = super().form_valid(form)
            return response
class CreateExamLog(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Exammodel
    fields = '__all__'
    template_name = "classes/exam.html"
    def get(self, request, *args, **kwargs):
        class ExamForm(forms.ModelForm):
                class Meta:
                    model = Exammodel
                    fields = '__all__'
        form = ExamForm()
        if "pk" in kwargs:
            form.initial['student'] = kwargs['pk']
            form.fields['student'].widget = forms.HiddenInput()
            form.fields['student'].label = ""
            form.fields["exam_date"].widget = widgets.DateInput(attrs={"type": "date"})
            
        return render(request, 'classes/exam.html', {'form': form})
    def post(self, request, *args, **kwargs):

           
            class ExamForm(forms.ModelForm):
                class Meta:
                    model = Exammodel
                    fields = '__all__'

            form = ExamForm(request.POST)
            
            if form.is_valid():
                return self.form_valid(form)
            
            return render(request, self.template_name, {'form': form})

    def form_valid(self, form):
            # Additional logic after the form is valid
            response = super().form_valid(form)
            return response
class CreateCertificateLog(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Certificatemodel
    fields = '__all__'
    template_name = "classes/certificate.html"
    def get(self, request, *args, **kwargs):
        class CertificateForm(forms.ModelForm):
                class Meta:
                    model = Certificatemodel
                    fields = '__all__'
        form = CertificateForm()
        if "pk" in kwargs:
            form.initial['student'] = kwargs['pk']
            form.fields['student'].widget = forms.HiddenInput()
            form.fields['student'].label = ""
            form.fields["date_of_complete"].widget = widgets.DateInput(attrs={"type": "date"})
            form.fields["certificate_date"].widget = widgets.DateInput(attrs={"type": "date"})
            form.fields["certificate_issued_date"].widget = widgets.DateInput(attrs={"type": "date"})
            
        return render(request, 'classes/certificate.html', {'form': form})
    def post(self, request, *args, **kwargs):

           
            class CertificateForm(forms.ModelForm):
                class Meta:
                    model = Certificatemodel
                    fields = '__all__'

            form = CertificateForm(request.POST)
            
            if form.is_valid():
                return self.form_valid(form)
            
            return render(request, self.template_name, {'form': form})

    def form_valid(self, form):
            # Additional logic after the form is valid
            response = super().form_valid(form)
            return response
def delete_book_log(request, pk):
    enquiry_log = get_object_or_404(Bookmodel, pk=pk)
    enquiry_log.delete()
    referring_url = request.META.get('HTTP_REFERER', '/')
    return redirect(referring_url) 
def delete_class_log(request, pk):
    enquiry_log = get_object_or_404(Classmodel, pk=pk)
    enquiry_log.delete()
    referring_url = request.META.get('HTTP_REFERER', '/')
    return redirect(referring_url) 
def delete_exam_log(request, pk):
    enquiry_log = get_object_or_404(Exammodel, pk=pk)
    enquiry_log.delete()
    referring_url = request.META.get('HTTP_REFERER', '/')
    return redirect(referring_url) 
def delete_certificate_log(request, pk):
    enquiry_log = get_object_or_404(Certificatemodel, pk=pk)
    enquiry_log.delete()
    referring_url = request.META.get('HTTP_REFERER', '/')
    return redirect(referring_url) 
class PublicAccessMixin(AccessMixin):
    def handle_no_permission(self):
        return super().handle_no_permission()


class PublicView(PublicAccessMixin,DetailView):
    model = Student
    template_name = "public/indexs.html"
    login_url = None
    def get_context_data(self, **kwargs):
        context = super(PublicView, self).get_context_data(**kwargs)
        context["payments"] = Invoice.objects.filter(student=self.object)
        context["booklog"] = Bookmodel.objects.filter(student=self.object)
        context["classlog"] = Classmodel.objects.filter(student=self.object)
        context["examlog"] = Exammodel.objects.filter(student=self.object)
        context["certilog"] = Certificatemodel.objects.filter(student=self.object)
        return context