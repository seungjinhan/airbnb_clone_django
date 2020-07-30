import random
from django.core.management.base import BaseCommand
from django.contrib.admin.utils import flatten
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
        created_photos = seeder.execute()
        created_clean = flatten(list(created_photos.values()))
        amenities = room_model.Amenity.objects.all()
        facilities = room_model.Facility.objects.all()

        for pk in created_clean:
            room = room_model.Room.objects.get(pk=pk)
            for i in range(3, random.randint(10, 17)):
                room_model.Photo.objects.create(
                    caption=seeder.faker.sentence(),
                    room=room,
                    file=f"/media/{random.randint(1,31)}.webp",
                )

            for a in amenities:
                num = random.randint(0, 15)
                if num % 2 == 0:
                    room.amenities.add(a)

            for a in facilities:
                num = random.randint(0, 15)
                if num % 2 == 0:
                    room.facilities.add(a)

        self.stdout.write(self.style.SUCCESS("Rooms created!"))
