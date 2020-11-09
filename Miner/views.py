from time import sleep

from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib import messages
from .forms import KeyForm


def index(request):
    return render(request, 'miner/index.html')


def keyList(request):

    return render(request, 'miner/key.html')


def newKey(request):
    key_form = KeyForm(request.POST or None)

    if(str(request.method) == 'POST'):
        if(key_form.is_valid()):
            keyName = key_form.cleaned_data['tokenname']
            key = key_form.cleaned_data['token']

            print(str(keyName) + ' '+str(key))

            messages.success(request, str('Key '+str(keyName)+' saved successfully!'))
            key_form = KeyForm()
        else:
            messages.error(request, 'Error in save')

    return render(request, 'miner/keyForm.html', {
        'form': key_form
    })
