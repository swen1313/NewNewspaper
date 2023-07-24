import logging
from datetime import timezone, timedelta

from django.conf import settings

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.template.loader import render_to_string
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution

from newspaper.models import Post

logger = logging.getLogger(__name__)





def send_mail():
    """ собственно отправка сообщений """
    # выбираем новости за прошедшие 7 дней
    new_posts = Post.objects.filter(
        created__gte=(timezone.now() - timedelta(days=7))
    )

    for user in User.objects.all():
        if user.email:

            user_new_post = new_posts.filter(category__in=user.category_set.all())
            if user_new_post:
                # подготовка шаблона и сообщения
                html_content = render_to_string(
                    'news_weekly.html',
                    {'posts': user_new_post, 'count': user_new_post.count(), 'user': user}
                )
                msg = EmailMultiAlternatives(
                    subject='News Paper. Новости за неделю',
                    body=f'Здравствуйте, {user.username}. Новости за неделю в вашей выбранной категории {{ category }} !',
                    from_email='yyulyul1@yandex.ru',
                    to=[user.email, ]
                )
                # привязка HTML и отправка
                msg.attach_alternative(html_content, "text/html")
                msg.send()



            # функция которая будет удалять неактуальные задачи
def delete_old_job_executions(max_age=604_800):
    """This job deletes all apscheduler job executions older than `max_age` from the database."""
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs apscheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        # добавляем работу нашему задачнику
        scheduler.add_job(
            my_job,
            trigger=CronTrigger(second="*/10"),
            # Тоже самое что и интервал, но задача тригера таким образом более понятна django
            id="my_job",  # уникальный айди
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'my_job'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),
            # Каждую неделю будут удаляться старые задачи, которые либо не удалось выполнить, либо уже выполнять не надо.
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info(
            "Added weekly job: 'delete_old_job_executions'."
        )

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")