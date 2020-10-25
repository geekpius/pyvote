from django import forms
from .models import Setting

class SettingForm(forms.ModelForm):

    class Meta:
        model = Setting
        fields = ['title', 'year', 'is_programme', 'is_department', 'is_house', 'is_form']

