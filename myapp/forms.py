from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from myapp.models import CartItems,MyOrders


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


class QunatityForm(forms.ModelForm):

    class Meta:

        model=CartItems

        fields=['quantity']

        widgets={

            'quantity':forms.NumberInput(attrs={'class':'w-10 border p-2','max': '5'})
        }

class CheckOutForm(forms.ModelForm):
    class Meta:
        model=MyOrders

        fields=['house_name','place','pincode','phone','payment_method']

        widgets={

           'house_name':forms.TextInput(attrs={'class':'w-full border p-2','placeholder': 'House name'}),
           'place':forms.TextInput(attrs={'class':'w-full border p-2','placeholder': 'Enter your place'}),
           'pincode':forms.NumberInput(attrs={'class':'w-full border p-2','placeholder': 'Enter 6-digit pincode'}),
           'phone':forms.TextInput(attrs={'class':'w-full border p-2','placeholder': 'Enter your mobile number'}),
           'payment_method':forms.Select(attrs={'class':'w-full border p-2'})

        }