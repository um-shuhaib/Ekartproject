from django import forms
from django.contrib.auth.models import User

class UserRegisterForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["first_name","username","password","email"]
        widgets={
            'first_name':forms.TextInput(attrs={'class':'form-control'}),
            'username':forms.TextInput(attrs={'class':'form-control'}),
            'password':forms.PasswordInput(attrs={'class':'form-control'}),
            'email':forms.EmailInput(attrs={'class':'form-control'}),
        }


class LoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username","password"]
        widgets={
            'username':forms.TextInput(attrs={'class':'form-control'}),
            'password':forms.PasswordInput(attrs={'class':'form-control'}),
        }