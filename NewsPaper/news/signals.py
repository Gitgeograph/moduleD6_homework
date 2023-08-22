from django.db.models.signals import m2m_changed
from django.dispatch import receiver 
from .models import PostCategory
from news.tasks import new_post_notification

@receiver(m2m_changed, sender=PostCategory)
def notify_subscribers_about_Post(sender, instance, action, **kwargs):
    if action == 'post_add':
        new_post_notification(instance)
    