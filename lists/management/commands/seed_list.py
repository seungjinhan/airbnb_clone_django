import random
from django.core.management.base import BaseCommand
from django_seed import Seed
from django.contrib.admin.utils import flatten
from lists.models import List
from users.models import User
from rooms.models import Room


class Command(BaseCommand):

    help = 'this command creates lists'

    def add_arguments(self, parser):
        parser.add_argument(
            '--number', default=2, type=int, help='how many lists do you want to create')

    def handle(self, *args, **options):
        number = options.get('number')
        seeder = Seed.seeder()

        users = User.objects.all()
        rooms = Room.objects.all()

        seeder.add_entity(List, number, {
            "user": lambda x: random.choice(users),
        },)

        created = seeder.execute()
        created_clean = flatten(list(created.values()))

        for pk in created_clean:
            list_model = List.objects.get(pk=pk)
            to_add = rooms[random.randint(0, 5): random.randint(6, 30)]
            list_model.rooms.add(*to_add)

        self.stdout.write(self.style.SUCCESS("Lists created!"))
