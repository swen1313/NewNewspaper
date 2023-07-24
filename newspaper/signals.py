from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from django.template.loader import render_to_string

from .models import Post, Category

@receiver(m2m_changed, sender=Post.category.through)
def send_email(sender, instance, **kwargs):

    if kwargs['action'] == "post_add" and kwargs["model"] == Category:
        for category in instance.category.all():
            for user in category.subscribers.all():
                if user.email:
                    html_content = render_to_string(
                        'news_notify.html',
                        {'post': instance, 'category': category, 'user': user}
                    )
                    msg = EmailMultiAlternatives(
                        subject = instance.title,
                        body=f'Здравствуйте, {user.username}. Вышла новая статья в выбранной ваши категории!',
                        from_email = 'yyulyul1@yandex.ru',
                        to = [user.email,]
                    )
                    msg.attach_alternative(html_content, "text/html")
                    msg.send()








