from django import forms
from .models import UserProfile
from django.contrib.auth.models import User



class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['profile_picture', 'phone_number', 'address', 'region', 'country','first_name','last_name']
        
class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email','password')
