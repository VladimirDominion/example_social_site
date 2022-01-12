from celery import shared_task


@shared_task
def morning_news(email):
    return f'send email to {email}'


@shared_task
def user_login(user_id):
    return f'User ID {user_id} enter'


@shared_task
def user_signup(user_id):
    return f'User ID {user_id} enter'


