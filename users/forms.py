from django import forms
from django.forms import ModelForm
from .models import Profile
from django.db.models import Q


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['name', 'phone', 'address', 'image']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control','placeholder':'Enter Your Name'}),
            'phone': forms.TextInput(attrs={'class': 'form-control','placeholder':'Start with 0'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
        }