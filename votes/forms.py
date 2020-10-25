from django import forms
from .models import VoteCart, Vote

class VoteCartForm(forms.ModelForm):
    class Meta:
        model = VoteCart
        fields = ['voter']

class VoteForm(forms.ModelForm):
    class Meta:
        model = Vote
        fields = ['voter']