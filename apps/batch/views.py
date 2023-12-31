from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import BatchModel
from .forms import BatchModelForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django import forms
from apps.course.models import *
class BatchListView(ListView):
    model = BatchModel
    template_name = "batch/batchlist.html"
    def slist(request):
        template_name = "batch/batchlist.html"
        return render(request, template_name , context={"batches":BatchModel.objects.all()})

class BatchDetailView(DetailView):
    model = BatchModel
    template_name = "batch/batchdetails.html"
    context_object_name = 'batch'
    def get_context_data(self, **kwargs):
        context = super(BatchDetailView, self).get_context_data(**kwargs)
        context["subject"] = CourseSubjectModel.objects.filter(course=self.object.batch_course)
        context["book"] = CourseBookModel.objects.filter(course=self.object.batch_course)
        context["exams"] = CourseExamModel.objects.filter(course=self.object.batch_course)
        return context

class BatchCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = BatchModel
    fields = '__all__'
    template_name = "batch/batchform.html"
    def get(self, request, *args, **kwargs):
        form = BatchModelForm()
    
            
        return render(request, 'batch/batchform.html', {'form': form})
    def post(self, request, *args, **kwargs):

            form = BatchModelForm(request.POST)
            
            if form.is_valid():
                return self.form_valid(form)
            
            return render(request, self.template_name, {'form': form})

    def form_valid(self, form):
            response = super().form_valid(form)
            return response

class BatchUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = BatchModel
    template_name = "batch/batchform.html"
    fields = "__all__"
    success_message = "Record successfully updated."

class BatchDeleteView(LoginRequiredMixin, DeleteView):
    model = BatchModel
    success_url = reverse_lazy("batch_list")

def delete_batchstudent_log(request, pk,id):
    enquiry_log = get_object_or_404(BatchModel, pk=pk)
    subject_to_remove = enquiry_log.batch_students.filter(id=id).first()
    if subject_to_remove:
        enquiry_log.batch_students.remove(subject_to_remove)
    referring_url = request.META.get('HTTP_REFERER', '/')
    return redirect(referring_url)


