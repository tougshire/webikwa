from django.core.management.base import BaseCommand, CommandError
from webikwa.models import IcalendarPage

class Command(BaseCommand):
    help = 'Auto saves pages - this is useful for pages like Icalendar page which update their data upon save'

    def add_arguments(self, parser):
        parser.add_argument('page_ids', nargs='+', type=int)

    def handle(self, *args, **options):
        for page_id in options['page_ids']:
            try:
                page = IcalendarPage.objects.get(pk=page_id)
            except page.DoesNotExist:
                raise CommandError('Page "%s" does not exist' % page_id)

            page.save() #this should automatically update the calendar

            self.stdout.write(self.style.SUCCESS('Successfully upated page "%s"' % page_id))