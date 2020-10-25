from django import forms
from .models import Voter, Programme

class VoterForm(forms.ModelForm):

    class Meta:
        model = Voter
        fields = ['access_number', 'name', 'gender', 'programme', 'department', 'house', 'form']


class VoterUpdateForm(forms.ModelForm):

    class Meta:
        model = Voter
        fields = ['name', 'gender', 'programme', 'department', 'house', 'form']


class ProgrammeCreateForm(forms.ModelForm):

    class Meta:
        model = Programme
        fields = ['name']