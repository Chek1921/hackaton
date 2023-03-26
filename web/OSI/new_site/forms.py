from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm

class RegForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Введите правильный email')

    class Meta:
        model = CustomUser
        fields = [
            'username',
            'first_name',
            'email', 
            'work_type',
            'password1', 
            'password2', 
            ]
        
# class WorkTypeForm(forms.ModelForm):
#     class Meta:
#         model = WorkType
#         filds = '__all__'