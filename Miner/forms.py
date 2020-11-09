from django import forms
from .models import Token, Miner

class KeyForm(forms.ModelForm):
    tokenname = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Example: John\'s key'}))
    token = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Example: 12345HSAHJ1243423'}))

    class Meta:
        model = Token
        fields = ['tokenname', 'token']

class MinerForm(forms.ModelForm):
    minername = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Example: Gold Miner rocks!!'}))  # Miner Name
    tokenassociated = forms.ModelChoiceField(queryset=Token.objects.all())

    class Meta:
        model = Miner
        fields = ['minername', 'tokenassociated', 'repo_list']