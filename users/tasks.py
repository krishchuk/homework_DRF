from celery import shared_task
from dateutil.relativedelta import relativedelta
from django.utils import timezone
from django.contrib.auth import get_user_model


@shared_task
def check_last_data():
    user = get_user_model()
    deadline_data = timezone.now() - relativedelta(months=1)
    inactive_users = user.objects.filter(last_login__lt=deadline_data, is_active=True)
    inactive_users.update(is_active=False)
