from django import forms
from django.contrib.auth.models import User

class UserRegisterForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["first_name","username","password","email"]
        widgets={
            'first_name':forms.TextInput(attrs={'class':'form-control'}),
            'username':forms.Textarea(attrs={'class':'form-control'}),
            'password':forms.DateInput(attrs={'class':'form-control'}),
            'email':forms.DateInput(attrs={'class':'form-control'}),
        }