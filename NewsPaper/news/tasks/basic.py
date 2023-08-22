from django.template.loader import render_to_string
from django.core.mail.message import EmailMultiAlternatives


def new_post_notification(instance):
    for category in instance.postCategory.all():
        for user in category.subscribers.all():

            html = render_to_string(
                template_name='mail/new_post_notification.html',
                context={
                    'category': category,
                    'post': instance,
                    'user': user,
                }
            )

            msg = EmailMultiAlternatives(
                subject=f'New post nottification',
                body="",
                from_email='Geographsawqa@yandex.ru',
                to=[user.email],
            )

            msg.attach_alternative(html, 'text/html')
            msg.send()