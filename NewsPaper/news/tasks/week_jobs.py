from django.template.loader import render_to_string
from django.core.mail.message import EmailMultiAlternatives
from datetime import timedelta
from django.utils import timezone
from news.models import Post, Category


def weekly_notification():
    date = timezone.now() - timedelta(weeks=1) 
    for category in Category.objects.all():
        for user in category.subscribers.all():                                 
            post_week = list(Post.objects.filter(postCategory = category, creationData__gte = date).order_by('-creationData'))

            html = render_to_string(
                template_name='mail/weekly_notification.html',
                context={
                    'posts_week': post_week,
                    'category': category,
                    'user': user
                }
            )

            msg = EmailMultiAlternatives(
                subject=f'Weekly news in the category {category}',
                body="",
                from_email='Geographsawqa@yandex.ru',
                to=[user.email],
            )

            msg.attach_alternative(html, 'text/html')
            msg.send()