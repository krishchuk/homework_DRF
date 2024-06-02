from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings


@shared_task
def send_mail_update(course=None, recipient_list=None):
    if recipient_list:
        send_mail(
            subject="Обновление курса на платформе!",
            message=f"Курс {course} был обновлен!",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=recipient_list,
            fail_silently=False,
        )
