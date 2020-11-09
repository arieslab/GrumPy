from django import forms
from .models import Token

class KeyForm(forms.ModelForm):
    tokenname = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Example: John\'s key'}))
    token = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Example: 12345HSAHJ1243423'}))

    class Meta:
        model = Token
        fields = ['tokenname', 'token']

