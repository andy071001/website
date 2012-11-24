from django.core.management.base import BaseCommand
from django.core.mail import EmailMultiAlternatives
from propaganda.models import Pamphlet
import sys, datetime

class Command(BaseCommand):
	help = """Send newsletter messages to the subscribers."""

	def handle(self, *args, **options):
		# Collect pamphlets
		today = datetime.date.today()
		pamphlets = Pamphlet.objects.filter(sent=False, delivery_date__gte=today).order_by("-delivery_date")

		# Compose emails
		for pamphlet in pamphlets:
			message = EmailMultiAlternatives(pamphlet.propaganda.subject, pamphlet.propaganda.plaintext_msg,
				pamphlet.propaganda.from_header, [pamphlet.subscriber.email,])
			message.attach_alternative(pamphlet.propaganda.html_msg, "text/html")
			try:
				message.send()
			except Exception, e:
				print >>sys.stderr, "Couldn't send pamphlet: %s" % unicode(e)
			else:
				pamphlet.sent = True
				pamphlet.save()
