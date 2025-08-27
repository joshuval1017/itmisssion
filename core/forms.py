from django import forms
from .models import Citizen
import re

class CitizenSignupForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, min_length=8)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Citizen
        fields = ['name', 'email', 'mobile', 'password', 'confirm_password']

    def clean_name(self):
        name = self.cleaned_data['name']
        if not re.match(r'^[A-Za-z\s]{2,}$', name):
            raise forms.ValidationError("Name must be at least 2 characters and contain only letters and spaces.")
        return name

    def clean_email(self):
        email = self.cleaned_data['email']
        if Citizen.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already registered.")
        return email

    def clean_mobile(self):
        mobile = self.cleaned_data['mobile']
        if not re.match(r'^\d{10,15}$', mobile):
            raise forms.ValidationError("Mobile number must be 10–15 digits.")
        return mobile

    def clean(self):
        cleaned_data = super().clean()
        pwd = cleaned_data.get('password')
        confirm = cleaned_data.get('confirm_password')

        if pwd != confirm:
            raise forms.ValidationError("Passwords do not match.")

        if not any(c.isdigit() for c in pwd) or not any(c.isalpha() for c in pwd):
            raise forms.ValidationError("Password must include both letters and numbers.")
