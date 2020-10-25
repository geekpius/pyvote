from django.contrib.auth import authenticate
from django import forms
from .models import User

class SigninForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ['username', 'password']

    def clean(self):
        if self.is_valid():
            username = self.cleaned_data['username']
            password = self.cleaned_data['password']
            if not authenticate(username=username, password=password):
                raise forms.ValidationError("Invalid login credentials.")


class AccountCreateForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ['username', 'name', 'password']
