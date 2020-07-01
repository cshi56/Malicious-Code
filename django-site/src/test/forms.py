from django import forms
from django.forms import ModelForm
from test.models import FileSubmission

class UploadFileForm(forms.Form):
    class Meta:
        model = FileSubmission
        fields = ['run_date', 'file']

    file = forms.FileField()
