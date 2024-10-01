from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms



class SignUpForm(UserCreationForm):
    password1=forms.CharField(widget=forms.PasswordInput(attrs={'class':'w-full border p-2 my-3'}))
    password2=forms.CharField(widget=forms.PasswordInput(attrs={'class':'w-full border p-2 my-3'}))
    class Meta:
        model=User
        fields=['username','email','password1','password2']
        widgets={
            'username':forms.TextInput(attrs={'class':'w-full border p-2 my-3'}),
            'email':forms.EmailInput(attrs={'class':'w-full border p-2 my-3'})
        }

class SignInForm(forms.Form):
    username=forms.CharField(widget=forms.TextInput(attrs={'class':'w-full border p-2 my-3'}))
    password=forms.CharField(widget=forms.PasswordInput(attrs={'class':'w-full border p-2 my-3'}))