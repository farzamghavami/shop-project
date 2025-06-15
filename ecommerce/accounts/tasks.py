from celery import shared_task
from time import sleep
from ecommerce.celery import Celery


@shared_task
def sendemail():
    sleep(3)
    print("sendemail done")