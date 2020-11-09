from django import forms


class KeyForm(forms.Form):
    tokenname = forms.CharField(label='Token Name', max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Example: John\'s key'}))
    token = forms.CharField(label='Token', max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Example: 12345HSAHJ1243423'}))
