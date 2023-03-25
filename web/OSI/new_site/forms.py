from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm

class RegForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Enter a valid email address')

    class Meta:
        model = CustomUser
        fields = [
            'username',
            'email', 
            'work_type',
            'password1', 
            'password2', 
            ]
        
# class WorkTypeForm(forms.ModelForm):
#     class Meta:
#         model = WorkType
#         filds = '__all__'