from django import forms
from .models import Job, Resume

class JobPostForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['title', 'description', 'skills_required', 'experience_required', 'location']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'skills_required': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Python, Django, SQL'}),
            'experience_required': forms.TextInput(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
        }

class ResumeUploadForm(forms.ModelForm):
    class Meta:
        model = Resume
        fields = ['file']
        widgets = {
            'file': forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': '.pdf,.docx'}),
        }
