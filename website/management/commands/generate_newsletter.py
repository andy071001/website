from django.core.management.base import BaseCommand
from django.core.mail import EmailMultiAlternatives
from propaganda.models import Propaganda, Subscriber, Pamphlet
import sys, datetime

class Command(BaseCommand):
	help = """Associate propaganda to subscribers creating a pamphlet."""

	def handle(self, *args, **options):
		# Fetch latest propaganda
		propaganda = Propaganda.objects.latest("id")

		# Check whether the latest propaganda was already sent
		pamphlets = Pamphlet.objects.filter(propaganda=propaganda, sent=True)
		if pamphlets.count() > 0:
			return

		subscribers = Subscriber.objects.filter(active=True)
		for subscriber in subscribers:
			try:
				pamphlet = Pamphlet.objects.get(propaganda=propaganda, \
						subscriber=subscriber, sent=False)
			except Pamphlet.DoesNotExist:
				pamphlet = Pamphlet.objects.create(propaganda=propaganda, \
						subscriber=subscriber, sent=False, \
						delivery_date = datetime.date.today())
				pamphlet.save()
			else:
				pamphlet.delivery_date = datetime.date.today()
				pamphlet.save()
