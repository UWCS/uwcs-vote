import logging
import requests
from defusedxml import ElementTree as ET
from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import transaction
from apscheduler.schedulers.blocking import BlockingScheduler
from django_apscheduler.jobstores import DjangoJobStore
from uwcs_auth.models import SUMember
import time

logger = logging.getLogger(__name__)

def fetch_webgroups(id):
    """
    Fetches the list of webgroups a user ID is in
    """
    url = f"https://webgroups.warwick.ac.uk/query/user/u{id}/groups"

    try:
        response = requests.get(url, timeout=7)
        if response.status_code == 200:
            try:
                root = ET.fromstring(response.content)
                groups = [
                    node.get('name')
                    for node in root.findall('group')
                    if node.get('name')
                ]
                return groups
            except ET.ParseError:
                print(f"Couldn't parse groups for {id}")
    except Exception as e:
        print(f"Unknown exception: {e}")
    return []

def sync_uwcs_members():
    """
    Fetches XML from Warwick SU API, syncs to DB.
    """
    api_key = getattr(settings, 'SU_API_KEY', '')
    url = f"https://www.warwicksu.com/membershipapi/listmembers/{api_key}/"

    print(f"Fetching members from: {url}")

    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()

        try:
            root = ET.fromstring(response.content)
        except ET.ParseError as e:
            print(f"Failed to parse XML: {e}")
            return

        member_nodes = root.findall('.//Member')

        valid_ids = []

        with transaction.atomic():
            for node in member_nodes:
                uid_node = node.find('UniqueID')
                fname_node = node.find('FirstName')
                lname_node = node.find('LastName')
                email_node = node.find('EmailAddress')

                if uid_node is None or not uid_node.text:
                    continue  # Skip invalid records / associate members

                uni_id = uid_node.text.strip()

                valid_ids.append(uni_id)

                SUMember.objects.update_or_create(
                    uniqueId=uni_id,
                    defaults={
                        'firstName': fname_node.text.strip() if (fname_node is not None and fname_node.text) else "",
                        'lastName': lname_node.text.strip() if (lname_node is not None and lname_node.text) else "",
                        'emailAddress': email_node.text.strip() if (email_node is not None and email_node.text) else "",
                    }
                )
            deleted_count, _ = SUMember.objects.exclude(uniqueId__in=valid_ids).delete()

        for new_id in valid_ids:
            print("Fetching for "+new_id)
            groups = fetch_webgroups(new_id)
            if groups:
                SUMember.objects.filter(uniqueId=new_id).update(webgroups=groups)
            time.sleep(0.1) # don't make IDG want to kill us

        print(f"Sync Complete. Active: {len(valid_ids)}. Removed: {deleted_count}.")

    except requests.RequestException as e:
        print(f"Network error during sync: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")


class Command(BaseCommand):
    help = "Fetch the SU members list"

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        print("Running initial sync...")
        sync_uwcs_members()

        scheduler.add_job(
            sync_uwcs_members,
            trigger="interval",
            hours=12,
            id="sync_members_job",
            max_instances=1,
            replace_existing=True,
        )

        try:
            print("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            print("Stopping scheduler...")
            scheduler.shutdown()