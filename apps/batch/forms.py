from django import forms
from .models import BatchModel

class BatchModelForm(forms.ModelForm):
    class Meta:
        model = BatchModel
        fields = '__all__'
        widgets = {
            'batch_start_date': forms.DateInput(attrs={'type': 'date'}),
            'batch_end_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('batch_start_date')
        end_date = cleaned_data.get('batch_end_date')

        # Perform additional validation if needed, e.g., ensure end date is after start date
        if start_date and end_date and end_date < start_date:
            raise forms.ValidationError("End date must be after start date")

        return cleaned_data
