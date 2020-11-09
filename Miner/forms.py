from django import forms
from .models import Token, Miner

class KeyForm(forms.ModelForm):
    tokenname = forms.CharField(label='Token Name', widget=forms.TextInput(attrs={'placeholder': 'Example: John\'s key'}))
    token = forms.CharField(label='Token', widget=forms.TextInput(attrs={'placeholder': 'Example: 12345HSAHJ1243423'}))

    class Meta:
        model = Token
        fields = ['tokenname', 'token']

class MinerForm(forms.ModelForm):
    minername = forms.CharField(label='Miner Name', widget=forms.TextInput(attrs={'placeholder': 'Example: Gold Miner rocks!!'}))  # Miner Name
    tokenassociated = forms.ModelChoiceField(label='Assign token to miner', queryset=Token.objects.all())
    repo_list = forms.CharField(label='Repository list to mine', widget=forms.Textarea(attrs={'placeholder': 'user01/repo01\nuser02/repo02\nuser03/repo03'}))

    class Meta:
        model = Miner
        fields = ['minername', 'tokenassociated', 'repo_list']