from django.core.management.base import BaseCommand

from healthier_food.db_filler import DbFiller


class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    # def add_arguments(self, parser):
    #     parser.add_argument('poll_id', nargs='+', type=int)

    def handle(self, *args, **options):
        DbFiller()
