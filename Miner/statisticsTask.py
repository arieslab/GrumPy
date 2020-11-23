from celery import shared_task
from celery.contrib.abortable import AbortableTask
from celery_progress.backend import ProgressRecorder
from .models import Repositories, Reactions, Event, Miner
from Miner.Issues_Persistence.Connections import Connections
from Miner.Issue_Management.Models.Model import RepositoryClass


@shared_task(bind=True, base=AbortableTask)
def repositoryStatisticCalculator(self, repolist, id):
    progress_recorder = ProgressRecorder(self)

    i = 0

    miner = Miner.objects.get(id=id)

    while(miner.minerstatus == 'Mining'):
        miner = Miner.objects.get(id=id)
        if(miner.minerstatus == 'Task aborted'):
            return 'Mined task aborted'
        repolist = miner.repo_list.split(' ')
        repolist.remove('')

        for repo in repolist:
            string = 'Creating the '+str(repo) + ' statistics.'
            progress_recorder.set_progress(i + 1, len(repolist), string)
            if self.is_aborted():
                return 'Task aborted'

            miner = Miner.objects.get(id=id)
            if (miner.minerstatus == 'Task aborted'):
                return 'Mined task aborted'

            REPO = Repositories.objects.get(reponame=repo)

            if(REPO.activitystatus == 'Finished' or REPO.activitystatus == 'Mining'):
                if self.is_aborted():
                    return 'Task aborted'

                #REPO = Repositories.objects.get(reponame=repo)

                dbRepo = RepositoryClass(repo)

                all_issues = dbRepo.getAmountOfIssues('all')
                Repositories.objects.filter(pk=REPO.id).update(amountMinedIssues=int(all_issues))

                open_issues = dbRepo.getAmountOfIssues('open')
                Repositories.objects.filter(pk=REPO.id).update(openIssues=int(open_issues))

                closed_issues = dbRepo.getAmountOfIssues('closed')
                Repositories.objects.filter(pk=REPO.id).update(closedIssues=int(closed_issues))

                all_issues_comments = dbRepo.getAmountOfComments('all')
                Repositories.objects.filter(pk=REPO.id).update(closedIssues=int(closed_issues))

                open_issues_comment = dbRepo.getAmountOfComments('open')
                Repositories.objects.filter(pk=REPO.id).update(amountOpenComments=int(open_issues_comment))

                closed_issues_comment = dbRepo.getAmountOfComments('closed')
                Repositories.objects.filter(pk=REPO.id).update(amountClosedComments=int(closed_issues_comment))

                reactions = dbRepo.getAmountOfReactions()

                if(Reactions.objects.filter(reponame=repo).count() > 0):
                    Reactions.objects.filter(reponame=repo).update(like=int(reactions['Like']))
                    Reactions.objects.filter(reponame=repo).update(heart=int(reactions['Heart']))
                    Reactions.objects.filter(reponame=repo).update(hooray=int(reactions['Hooray']))
                    Reactions.objects.filter(reponame=repo).update(confused=int(reactions['Confused']))
                    Reactions.objects.filter(reponame=repo).update(deslike=int(reactions['Deslike']))
                    Reactions.objects.filter(reponame=repo).update(laught=int(reactions['Laugh']))
                    Reactions.objects.filter(reponame=repo).update(rocket=int(reactions['Rocket']))
                    Reactions.objects.filter(reponame=repo).update(eyes=int(reactions['Eyes']))

                else:
                    Reactions_Instance = Reactions()

                    Reactions_Instance.reponame = repo
                    Reactions_Instance.like = reactions['Like']
                    Reactions_Instance.heart = reactions['Heart']
                    Reactions_Instance.hooray = reactions['Hooray']
                    Reactions_Instance.confused = reactions['Confused']
                    Reactions_Instance.deslike = reactions['Deslike']
                    Reactions_Instance.laught = reactions['Laugh']
                    Reactions_Instance.rocket = reactions['Rocket']
                    Reactions_Instance.eyes = reactions['Eyes']

                    Reactions_Instance.save()

                events = dbRepo.getTop10OfEvents()

                if (Event.objects.filter(reponame=repo).count() > 0):
                    Event.objects.filter(reponame=repo).update(eventname_1=str(events[0][0]))
                    Event.objects.filter(reponame=repo).update(amountOfEvent_1=int(events[0][1]))

                    Event.objects.filter(reponame=repo).update(eventname_2=str(events[1][0]))
                    Event.objects.filter(reponame=repo).update(amountOfEvent_2=int(events[1][1]))

                    Event.objects.filter(reponame=repo).update(eventname_3=str(events[2][0]))
                    Event.objects.filter(reponame=repo).update(amountOfEvent_3=int(events[2][1]))

                    Event.objects.filter(reponame=repo).update(eventname_4=str(events[3][0]))
                    Event.objects.filter(reponame=repo).update(amountOfEvent_4=int(events[3][1]))

                    Event.objects.filter(reponame=repo).update(eventname_4=str(events[4][0]))
                    Event.objects.filter(reponame=repo).update(amountOfEvent_4=int(events[4][1]))

                else:
                    Event_Instance = Event()

                    Event_Instance.reponame = repo

                    Event_Instance.eventname_1 = events[0][0]
                    Event_Instance.amountOfEvent_1 = events[0][1]

                    Event_Instance.eventname_2 = events[1][0]
                    Event_Instance.amountOfEvent_2 = events[1][1]

                    Event_Instance.eventname_3 = events[2][0]
                    Event_Instance.amountOfEvent_3 = events[2][1]

                    Event_Instance.eventname_4 = events[3][0]
                    Event_Instance.amountOfEvent_4 = events[3][1]

                    Event_Instance.eventname_5 = events[4][0]
                    Event_Instance.amountOfEvent_5 = events[4][1]

                    Event_Instance.save()
            i += 1

    print('Statistics finished')
    return 'Statistics finished'
