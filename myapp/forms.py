from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from myapp.models import CartItems,MyOrders,Reviews


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

            'quantity':forms.NumberInput(attrs={'class':'w-10 border p-2'})
        }
    


class CheckOutForm(forms.ModelForm):
    class Meta:
        model=MyOrders

        fields=['house_name','place','pincode','phone','payment_method']

        widgets={

           'house_name':forms.TextInput(attrs={'class':'w-full border p-2','placeholder': 'House name'}),
           'place':forms.TextInput(attrs={'class':'w-full border p-2','placeholder': 'Enter your place'}),
           'pincode':forms.NumberInput(attrs={'class':'w-full border p-2','placeholder': 'Enter 6-digit pincode', 'max_length':'6'}),
           'phone':forms.TextInput(attrs={'class':'w-full border p-2','placeholder': 'Enter your mobile number'}),
           'payment_method':forms.Select(attrs={'class':'w-full border p-2'})
        }

class ReviewForm(forms.ModelForm):

    class Meta:

        model=Reviews
        
        fields=['comment','rating']

        widgets={
            'comment':forms.Textarea(attrs={'class':'w-full border p-2' ,"rows":5}),
            'rating':forms.NumberInput(attrs={'class':'w-full border p-2'})
        }

class SearchForm(forms.Form):

   query = forms.CharField(label='Search', max_length=100, required=False)