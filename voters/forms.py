from django import forms
from .models import Voter

class VoterForm(forms.ModelForm):

    class Meta:
        model = Voter
        fields = ['access_number', 'name', 'gender', 'department']


class VoterUpdateForm(forms.ModelForm):

    class Meta:
        model = Voter
        fields = ['name', 'gender', 'department']
