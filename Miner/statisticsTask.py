from celery import shared_task
from celery.contrib.abortable import AbortableTask
from celery_progress.backend import ProgressRecorder


@shared_task(bind=True, base=AbortableTask)
def repositoryStatisticCalculator(self):
    pass