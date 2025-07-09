from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import get_user_model
import re

User = get_user_model()

class CustomRegistrationForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
       
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already exists")
        return email

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        errors = []
        if len(password1) < 8:
            errors.append('Password must be at least 8 characters long')
        if not re.search(r'[A-Z]', password1):
            errors.append('Must contain an uppercase letter')
        if not re.search(r'[a-z]', password1):
            errors.append('Must contain a lowercase letter')
        if not re.search(r'[0-9]', password1):
            errors.append('Must contain a number')
        if not re.search(r'[@#$%^&+=]', password1):
            errors.append('Must contain a special character')
        if errors:
            raise forms.ValidationError(errors)
        return password1

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get('password1') != cleaned_data.get('confirm_password'):
            raise forms.ValidationError("Passwords do not match")
        return cleaned_data
    def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            # Remove help_text for username field
            self.fields['username'].help_text = None

class LoginForm(AuthenticationForm):
    pass  # You can customize here if needed
