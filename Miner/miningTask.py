from time import sleep

import requests
from requests import exceptions
from github import Github, GithubException
from celery import shared_task
from celery_progress.backend import ProgressRecorder

@shared_task(bind=True)
def test_worker(self, NAME):
    progress_recorder = ProgressRecorder(self)
    i = 0
    total = 50
    while(i < 20):
        string = str(NAME) + ' Testing task - Downloading'
        progress_recorder.set_progress(i + 1, total, string)
        sleep(3)
        i += 1


    return str(NAME) + 'Testing task - Task finished'

@shared_task(bind=True)
def mining_worker(self):
    pass