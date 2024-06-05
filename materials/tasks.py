from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

from materials.models import Subscription


@shared_task
def send_mail_update(course_id):
    subscriptions = [sub.user.email for sub in Subscription.objects.filter(course_id=course_id)]
    send_mail(
        subject="Обновление курса на платформе!",
        message=f"Курс {subscriptions.course.title} был обновлен!",
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=subscriptions,
        fail_silently=False,
    )
