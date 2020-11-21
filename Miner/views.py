from time import sleep
from celery import app
from celery.contrib.abortable import AbortableAsyncResult
from celery.contrib.pytest import celery_app
from celery.result import AsyncResult
#from celery.worker.control import revoke, terminate
from GrumPy.celery import app

from django.views.decorators.csrf import csrf_exempt
from Miner.Issue_Management.Models.Model import RepositoryClass, IssueIndex
from .miningTask import mining_worker, test_worker

from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import KeyForm, MinerForm
from .models import Token, Miner
from Miner.Issues_Persistence.Connections import Connections

celery_tasks = []


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


@csrf_exempt
def newKey(request):
    key_form = KeyForm(request.POST or None)

    if (str(request.method) == 'POST'):
        if (key_form.is_valid()):
            # token_model = Token()

            keyName = key_form.cleaned_data['tokenname']
            # token_model.key = key_form.cleaned_data['token']

            key_form.save()

            messages.success(request, str('Key ' + str(keyName) + ' saved successfully!'))
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
        messages.info(request, str('Token removed!'))
    # return render(request, 'miner/key.html', {'tokens': Token.objects.all()})

    return HttpResponseRedirect('/keys')


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

            # print(str(token_id))
            # miner_form.save()

            messages.success(request, str('Minder ' + str(minerName) + ' saved successfully!'))
            miner_form = MinerForm()
        else:
            messages.error(request, 'Error in save')

    return render(request, 'miner/minerForm.html', {
        'form': miner_form
    })


def teste(request):
    return render(request, 'miner/teste.html')


def issues(request):
    connection_instance = Connections()
    ListOfRepos = []

    for repo in connection_instance.getListOfRepo():
        repo_instance = RepositoryClass(repo)

        ListOfRepos.append(repo_instance)

    connection_instance.closeConnectionToDB()

    context = {
        'Repos_list': ListOfRepos
    }

    return render(request, 'miner/issues.html', context)


class Test:
    def __init__(self, lista):
        self.lista = lista


def dashboard(request):
    connection_instance = Connections()

    openedIssues = connection_instance.getAmountOfIssuesInDBByStatus('open')
    closedIssues = connection_instance.getAmountOfIssuesInDBByStatus('closed')
    amountOfRepos = connection_instance.getAmountOfRepos()

    amountOfIssues = openedIssues + closedIssues

    connection_instance.closeConnectionToDB()

    testeLista = Test([openedIssues, closedIssues])

    context = {
        'test': testeLista,
        'amountOfRepos': amountOfRepos,
        'amountOfIssues': amountOfIssues
    }

    return render(request, 'miner/dashboard.html', context)


def startMining(request, id):
    if (str(request.method) == 'POST'):
        miner = Miner.objects.get(id=id)
        # m_worker = test_worker.delay(miner.minername, id)
        m_worker = mining_worker.delay(id)
        celery_tasks.append(m_worker)
        Miner.objects.filter(pk=id).update(minertaskid=m_worker.task_id)
        Miner.objects.filter(pk=id).update(minerstatus='Mining...')

        print('Start ' + str(miner.minername))

    context = {
        'miners': Miner.objects.all(),
        'tokens': Token.objects.all(),
    }

    return HttpResponseRedirect('/miners')


def stopMining(request, id):
    if (str(request.method) == 'POST'):
        miner = Miner.objects.get(id=id)
        print(str(miner.minertaskid))

        id_worker = miner.minertaskid
        worker = AbortableAsyncResult(id_worker)
        print(worker.is_aborted())
        worker.abort()
        print(worker.is_aborted())

        Miner.objects.filter(pk=id).update(minerstatus='Task aborted')

    return HttpResponseRedirect('/miners')


def deleteMiner(request, id):
    if (str(request.method) == 'POST'):
        miner = Miner.objects.get(id=id)
        miner.delete()

    context = {
        'miners': Miner.objects.all(),
        'tokens': Token.objects.all()
    }

    return HttpResponseRedirect('/miners')


def viewprogress(request, id):
    print(str(id))

    miner = Miner.objects.get(id=id)

    context = {
        'minerName': miner.minername,
        'tokenAssociated': miner.tokenassociated,
        'task_id': miner.minertaskid
    }

    return render(request, 'miner/viewMinerProgress.html', context)


def MainStatistics(request):
    connection_instance = Connections()
    ListOfRepos = []

    for repo in connection_instance.getListOfRepo():
        repo_instance = RepositoryClass(repo)

        ListOfRepos.append(repo_instance)

    connection_instance.closeConnectionToDB()

    context = {
        'Repos_list': ListOfRepos
    }

    return render(request, 'miner/StatisticsIndex.html', context)


def showListOfIssues(request, reponame):
    r_name = reponame.replace('%2F', '/')
    connection_instance = Connections()

    ListOfIssues = []

    for i in connection_instance.getListOfIssues(r_name):
        IssueAtt = IssueIndex(r_name,
                              i['Id'],
                              i['Status'],
                              len(i['Reactions']),
                              (int(i['Reactions'].get('Like')) +
                               int(i['Reactions'].get('Heart')) +
                               int(i['Reactions'].get('Hooray')) +
                               int(i['Reactions'].get('Confused')) +
                               int(i['Reactions'].get('Deslike')) +
                               int(i['Reactions'].get('Laugh')) +
                               int(i['Reactions'].get('Rocket')) +
                               int(i['Reactions'].get('Eyes'))),
                              len(i['Events']))

        ListOfIssues.append(IssueAtt)

    context = {
        'Issues_List': ListOfIssues
    }

    return render(request, 'miner/showListOfIssues.html', context)
