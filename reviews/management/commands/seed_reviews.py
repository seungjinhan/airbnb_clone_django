import random
from django.core.management.base import BaseCommand
from django_seed import Seed
from reviews.models import Review
from users.models import User
from rooms.models import Room


class Command(BaseCommand):

    help = 'this command creates reviews'

    def add_arguments(self, parser):
        parser.add_argument(
            '--number', default=2, type=int, help='how many reviews do you want to create')

    def handle(self, *args, **options):
        number = options.get('number')
        seeder = Seed.seeder()

        users = User.objects.all()
        rooms = Room.objects.all()

        seeder.add_entity(Review, number, {
            'accuracy': lambda x: random.randint(0, 6),
            'communication': lambda x: random.randint(0, 6),
            'cleanlines': lambda x: random.randint(0, 6),
            'location': lambda x: random.randint(0, 6),
            'check_in': lambda x: random.randint(0, 6),
            'value': lambda x: random.randint(0, 6),
            "room": lambda x: random.choice(rooms),
            "user": lambda x: random.choice(users),
        })

        seeder.execute()
        self.stdout.write(self.style.SUCCESS("Reviews created!"))
