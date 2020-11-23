from time import sleep
from celery import app
from celery.contrib.abortable import AbortableAsyncResult
from celery.contrib.pytest import celery_app
from celery.result import AsyncResult
# from celery.worker.control import revoke, terminate
from GrumPy.celery import app
from Miner.statisticsTask import repositoryStatisticCalculator

from django.views.decorators.csrf import csrf_exempt
from Miner.Issue_Management.Models.Model import RepositoryClass, IssueIndex, Issue
from .miningTask import mining_worker, test_worker

from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import KeyForm, MinerForm
from .models import Token, Miner, Repositories, Event, Reactions
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
            repoList = miner_form.cleaned_data['repo_list'].split()
            token_id = Token.objects.filter(tokenname=tokenAssociated).values_list('id', flat=True).first()

            miner.minername = str(minerName)
            miner.tokenassociated = tokenAssociated
            miner.repoamount = 0
            miner.minedamount = 0
            miner.minerstatus = "Waiting"
            miner.minertaskid = '-'

            repository_list = ''

            for repo in repoList:
                repository_list += repo + ' '

                if (Repositories.objects.filter(reponame=repo).count() > 0):
                    Repositories.objects.filter(reponame=repo).update(activitystatus=str('Waiting'))
                    Repositories.objects.filter(reponame=repo).update(associatedMiner=str(minerName))
                else:
                    repositoryInstance = Repositories()
                    repositoryInstance.reponame = repo
                    repositoryInstance.activitystatus = 'Waiting'
                    repositoryInstance.firstissuenumber = repositoryInstance.lastissuenumber = 0
                    repositoryInstance.openIssues = repositoryInstance.closedIssues = 0
                    repositoryInstance.amountOpenReactions = repositoryInstance.amountClosedReactions = 0
                    repositoryInstance.amountOpenComments = repositoryInstance.amountClosedComments = 0

                    repositoryInstance.associatedMiner = str(minerName)
                    repositoryInstance.currentminingissue = repositoryInstance.amountMinedIssues = 0
                    repositoryInstance.associatedStatisticWorker = '-'
                    repositoryInstance.save()

            miner.repo_list = repository_list

            miner.save()

            messages.success(request, str('Miner ' + str(minerName) + ' saved successfully!'))
            miner_form = MinerForm()
        else:
            messages.error(request, 'Error in save')

    return render(request, 'miner/minerForm.html', {
        'form': miner_form
    })


def teste(request):
    return render(request, 'miner/teste.html')


def detailed_issue(request):
    return render(request, 'miner/detailed_issue.html')


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

    reactions_list = Reactions.objects.all()

    reactions = {
        'Like': 0, 'Heart': 0, 'Hooray': 0, 'Confused': 0, 'Deslike': 0, 'Laugh': 0, 'Rocket': 0, 'Eyes': 0
    }

    for reaction in reactions_list:
        print(reaction.reponame)

        reactions['Like'] += reaction.like
        reactions['Heart'] += reaction.heart
        reactions['Hooray'] += reaction.hooray
        reactions['Confused'] += reaction.confused
        reactions['Deslike'] += reaction.deslike
        reactions['Laugh'] += reaction.laught
        reactions['Rocket'] += reaction.rocket
        reactions['Eyes'] += reaction.eyes

    comments = 0

    repos_list = Repositories.objects.all()

    for repo in repos_list:
        if(repo.amountOpenComments != None):
            comments += repo.amountOpenComments
        if (repo.amountClosedComments != None):
            comments += repo.amountClosedComments

    l = {'subscribed': 0, 'mentioned': 0, 'referenced': 0, 'labeled': 0, 'closed': 0, 'assigned': 0,
         'merged': 0, 'milestoned':0, 'reopened': 0}

    event_list = Event.objects.all()

    for e in event_list:
        l[e.eventname_1] += e.amountOfEvent_1
        l[e.eventname_2] += e.amountOfEvent_2
        l[e.eventname_3] += e.amountOfEvent_3
        l[e.eventname_4] += e.amountOfEvent_4
        l[e.eventname_5] += e.amountOfEvent_5


    context = {
        'test': testeLista,
        'amountOfRepos': amountOfRepos,
        'amountOfIssues': amountOfIssues,
        'like': reactions['Like'],
        'heart': reactions['Heart'],
        'hooray': reactions['Hooray'],
        'confused': reactions['Confused'],
        'deslike': reactions['Deslike'],
        'laugh': reactions['Laugh'],
        'rocket': reactions['Rocket'],
        'eyes': reactions['Eyes'],
        'amountOfComments': comments,
        'subscribed': l['subscribed'],
        'mentioned': l['mentioned'],
        'referenced': l['referenced'],
        'labeled': l['labeled'],
        'closed': l['closed']
        }
    return render(request, 'miner/dashboard.html', context)


def startMining(request, id):
    if (str(request.method) == 'POST'):
        miner = Miner.objects.get(id=id)

        # m_worker = test_worker.delay(miner.minername, id)

        m_worker = mining_worker.delay(id)
        celery_tasks.append(m_worker)
        Miner.objects.filter(pk=id).update(minertaskid=m_worker.task_id)
        Miner.objects.filter(pk=id).update(minerstatus='Mining')

        repolist = miner.repo_list

        repositories_list = repolist

        s_worker = repositoryStatisticCalculator.delay(repositories_list, id)

        Miner.objects.filter(pk=id).update(statisticstaskid=s_worker.task_id)

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

        id_statistics_worker = miner.statisticstaskid
        statistics_worker = AbortableAsyncResult(id_statistics_worker)
        statistics_worker.abort()

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
    connection_instance.closeConnectionToDB()
    context = {
        'Issues_List': ListOfIssues
    }

    return render(request, 'miner/showListOfIssues.html', context)


def IssueDetail(request, reponame, id):
    # print(str(reponame))
    # print(id)

    issue = Issue(str(reponame), int(id))

    context = {
        'Issue': issue
    }

    return render(request, 'miner/detailed_issue.html', context)


def repositoryDashboard(request, reponame):
    r_name = reponame.replace('%2F', '/')
    print(r_name)

    repository = Repositories.objects.get(reponame=r_name)
    events = Event.objects.get(reponame=r_name)
    reactions = Reactions.objects.get(reponame=r_name)



    print(repository.reponame)
    amount_of_issues = repository.openIssues + repository.closedIssues

    amount_of_comments = repository.amountOpenComments + repository.amountClosedComments

    context = {
        'repository': repository,
        'events': events,
        'reactions': reactions,
        'amountIssues': amount_of_issues,
        'amountComments': amount_of_comments
    }

    return render(request, 'miner/repositoryDashboard.html', context)
