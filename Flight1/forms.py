from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm


class PasswordChangingForm(PasswordChangeForm):
        old_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control','placeholder': 'Old Password *'}))
        new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control','placeholder': 'New Password *'}))
        new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control','placeholder': 'New Password Confirmation *'}))
        class Meta:
            model = User
            fields =['old_password', 'new_password1', 'new_password2']

