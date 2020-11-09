from time import sleep

from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import KeyForm, MinerForm
from .models import Token, Miner

def index(request):
    context = {
        'miners': Miner.objects.all(),
        'tokens': Token.objects.all()
    }

    return render(request, 'miner/index.html', context)


def keyList(request):
    context = {
        'tokens': Token.objects.all()
    }
    return render(request, 'miner/key.html', context)


def newKey(request):
    key_form = KeyForm(request.POST or None)

    if(str(request.method) == 'POST'):
        if(key_form.is_valid()):
            #token_model = Token()

            keyName = key_form.cleaned_data['tokenname']
            #token_model.key = key_form.cleaned_data['token']

            key_form.save()

            messages.success(request, str('Key '+str(keyName)+' saved successfully!'))
            key_form = KeyForm()
        else:
            messages.error(request, 'Error in save')

    return render(request, 'miner/keyForm.html', {
        'form': key_form
    })

def deleteKey(request, id):
    if (str(request.method) == 'POST'):
        token = Token.objects.get(id=id)
        token.delete()
    return render(request, 'miner/key.html', {'tokens': Token.objects.all()})

def newMiner(request):
    miner_form = MinerForm(request.POST or None)

    if (str(request.method) == 'POST'):
        if (miner_form.is_valid()):
            miner = Miner()

            minerName = miner_form.cleaned_data['minername']
            # token_model.key = key_form.cleaned_data['token']
            tokenAssociated = miner_form.cleaned_data['tokenassociated']
            repoList = miner_form.cleaned_data['repo_list']
            token_id = Token.objects.filter(tokenname=tokenAssociated).values_list('id', flat=True).first()

            miner.minername = str(minerName)
            miner.tokenassociated = tokenAssociated
            miner.repoamount = 0
            miner.minedamount = 0
            miner.minerstatus = "Waiting"
            miner.minertaskid = '-'
            miner.repo_list = repoList
            miner.save()

            #print(str(token_id))
            #miner_form.save()

            messages.success(request, str('Minder ' + str(minerName) + ' saved successfully!'))
            miner_form = MinerForm()
        else:
            messages.error(request, 'Error in save')

    return render(request, 'miner/minerForm.html', {
        'form': miner_form
    })


