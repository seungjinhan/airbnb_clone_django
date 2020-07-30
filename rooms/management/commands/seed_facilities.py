from django.core.management.base import BaseCommand
from rooms.models import Facility


class Command(BaseCommand):

    help = 'this command creates facilites'

    # def add_arguments(self, parser):
    #     parser.add_argument(
    #         '--times', help='how many time do you want me to tell')

    def handle(self, *args, **options):
        facilities = [
            "Private entrance",
            "Paid parking on premises",
            "Paid parking off premises",
            "Elevator",
            "Parking",
            "Gym",
        ]
        for f in facilities:
            Facility.objects.create(name=f)
        self.stdout.write(self.style.SUCCESS(
            f"{len(facilities)} facilities created!"))
