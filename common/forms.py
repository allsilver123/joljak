# common/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class SignUpForm(UserCreationForm):
    phone_number = forms.CharField(max_length=20, required=False)

    class Meta:
        model = CustomUser
        fields = ['username', 'password1', 'password2', 'phone_number']
