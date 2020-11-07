from django import forms
from .models import Position, Candidate

class PositionForm(forms.ModelForm):

    class Meta:
        model = Position
        fields = ['name', 'position_type', 'max_con', 'winning_format']


class CandidateForm(forms.ModelForm):

    class Meta:
        model = Candidate
        fields = ['name', 'gender', 'position', 'department', 'image']


class CandidateUpdateForm(forms.ModelForm):

    class Meta:
        model = Candidate
        fields = ['name', 'gender', 'position', 'department']

class CandidateImageUpdateForm(forms.ModelForm):

    class Meta:
        model = Candidate
        fields = ['image']