from time import sleep
from venv import logger

import requests
from requests import exceptions
from github import Github, GithubException
from celery import shared_task
from celery_progress.backend import ProgressRecorder
from celery.task.control import revoke
from Miner.Activity_performance import MinersClass, RequestVerificationClass
from Miner.Issues_Persistence.Connections import Connections
from celery.contrib.abortable import AbortableTask

from Miner.models import Miner


@shared_task(bind=True, base=AbortableTask)
def test_worker(self, NAME, miner_id):
    progress_recorder = ProgressRecorder(self)
    i = 0
    total = 50
    while (i < 20):
        if self.is_aborted():
            return 'Task aborted'
        string = str(NAME) + ' Testing task - Downloading'
        progress_recorder.set_progress(i + 1, total, string)
        sleep(3)
        i += 1

    Miner.objects.filter(pk=miner_id).update(minerstatus='Finished')
    return str(NAME) + 'Testing task - Task finished'

@shared_task(bind=True)
def mining_worker(self, miner):
    authentication = Github(miner.tokenassociated.tokenname)
    connectionToDB = Connections()
    connectionToDB.openConnectionToDB()

    for repo in miner.repo_list:
        first_issue = last_issue = 0

        ISSUE_extrac = MinersClass(authentication, 1800, 5)

        last_issue = ISSUE_extrac.getLastIssue(repo)

        if (last_issue is not None):
            if (connectionToDB.verifyCollectionInDatabase(repo) == True):
                try:
                    first_issue = connectionToDB.verifyLastIssueInCollection(repo)
                except:
                    raise SystemError('Error finding the first repo issue')

    connectionToDB.closeConnectionToDB()
