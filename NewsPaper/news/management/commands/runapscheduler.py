import logging

from django.conf import settings

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django.utils import timezone
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution

from ...tasks import weekly_notify_for_new_posts

logger = logging.getLogger(__name__)


def weekly_notify_for_news_job():
    print(f'Begin weekly mailing for new posts')
    weekly_notify_for_new_posts()
    print(f'End weekly mailing for new posts')
    pass


def delete_old_job_executions(max_age=864_000):
    """This job deletes all apscheduler job executions
    older than `max_age` from the database."""
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs apscheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(
            weekly_notify_for_news_job,
            trigger=CronTrigger(
                day_of_week='mon', hour='00', minute='00'
            ),
            id='weekly_notify_for_news_job',
            max_instances=1,
            replace_existing=True,
        )
        logger.info('Added job: "Weekly notify for new posts"')

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="sun", hour="00", minute="00"
            ),
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
