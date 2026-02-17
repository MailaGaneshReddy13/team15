from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class RoleSelectionForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['role']
        widgets = {
            'role': forms.Select(attrs={'class': 'form-select'}),
        }

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('email', 'role', 'phone', 'organization_name', 'profile_picture')
        widgets = {
            'role': forms.Select(attrs={'class': 'form-select', 'id': 'role-select'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'organization_name': forms.TextInput(attrs={'class': 'form-control', 'id': 'org-name-field', 'placeholder': 'Company/Organization Name'}),
            'profile_picture': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
