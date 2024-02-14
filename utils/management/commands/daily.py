from django.core.management.base import BaseCommand
from django.db.models import Count
from messaging.models import MessageThread
from notifications.tasks import doSummaryNotificationMailings
from users.utils import updateMemberships


class Command(BaseCommand):
    help = "Performs all daily cleanup tasks"

    def handle(self, *args, **options):
        doSummaryNotificationMailings()
        MessageThread.objects.annotate(Count("message")).filter(
            message__count=0
        ).all().delete()
        self.stdout.write("Messages Thread Cleaned")
        updateMemberships()
        self.stdout.write("Memberships updated")
