from celery import shared_task


@shared_task
def morning_news(email):
    return 'success'


