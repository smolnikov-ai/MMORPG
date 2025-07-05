import datetime

from celery import shared_task
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string

from MMORPG import settings
from .models import Reply, Advertisement, User


@shared_task
def notify_reply_added(reply_pk):
    reply = Reply.objects.get(pk=reply_pk)
    ad = reply.advertisement
    subject = f'Reply of the advertisement {ad}'
    message = f'New reply from {reply.user}\\n{reply.content}'
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [ad.user.email]
    send_mail(subject, message, from_email, recipient_list, fail_silently=True)

@shared_task
def notify_reply_accepted(reply_pk):
    reply = Reply.objects.get(pk=reply_pk)
    ad = reply.advertisement
    subject = f'Reply of the advertisement {ad}'
    message = f'Your reply has been accepted\\n{reply.content}'
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [reply.user.email]
    send_mail(subject, message, from_email, recipient_list, fail_silently=True)

@shared_task
def notify_reply_delete(reply_pk):
    reply = Reply.objects.get(pk=reply_pk)
    ad = reply.advertisement
    subject = f'Reply of the advertisement {ad}'
    message = f'Your reply has been deleted\\n{reply.content}'
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [reply.user.email]
    send_mail(subject, message, from_email, recipient_list, fail_silently=True)

@shared_task
def send_weekly():
    today = datetime.datetime.now()
    last_week = today - datetime.timedelta(weeks=1)
    ads = Advertisement.objects.filter(creqtion_date__gte=last_week)
    users = User.objects.filter(is_active=True)

    for user in users:
        html_content = render_to_string(
            'daily_ads.html',
            {
                'username': user.username,
                'ads': ads,
                'link': settings.SITE_URL,
            }
        )

        msg = EmailMultiAlternatives(
            subject='Advertisement Report',
            body="",
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[user.email],
        )

        msg.attach_alternative(html_content, "text/html")
        msg.send()

