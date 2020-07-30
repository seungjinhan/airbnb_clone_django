import random
from django.core.management.base import BaseCommand
from django_seed import Seed
from rooms import models as room_model
from users import models as user_model


class Command(BaseCommand):

    help = 'this command creates users'

    def add_arguments(self, parser):
        parser.add_argument(
            '--number', default=2, type=int, help='how many users do you want to create')

    def handle(self, *args, **options):
        number = options.get('number')
        seeder = Seed.seeder()

        all_user = user_model.User.objects.all()
        room_types = room_model.RoomType.objects.all()

        seeder.add_entity(room_model.Room, number, {
            'name': lambda x: seeder.faker.address(),
            'host': lambda x:  random.choice(all_user),
            'room_type': lambda x: random.choice(room_types),
            "guests": lambda x: random.randint(0, 20),
            'price': lambda x: random.randint(0, 300),
            'beds': lambda x: random.randint(0, 5),
            'bedrooms': lambda x: random.randint(0, 5),
            'baths': lambda x: random.randint(0, 5),
        })
        seeder.execute()
        self.stdout.write(self.style.SUCCESS("Rooms created!"))
