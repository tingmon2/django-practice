import random
from django.core.management.base import BaseCommand  # 내가 만든 core 앱이랑은 관계없는 장고 안의 core임
from django_seed import Seed
from django.contrib.admin.utils import flatten
from rooms import models as room_models
from users import models as user_models


class Command(BaseCommand):
    help = "create rooms"

    # 몇 명의 유저를 만들 것 인지 지시하기 위해 아규먼트를 더함
    def add_arguments(self, parser):
        parser.add_argument("--number", type=int, default=1, help="How many rooms?")

    # 받아온 숫자만큼 유저를 만드는데 스태프와 관리자가 아니어야 함
    def handle(self, *args, **options):
        number = options.get("number")
        seeder = Seed.seeder()
        all_users = user_models.User.objects.all()
        room_types = room_models.RoomType.objects.all()

        seeder.add_entity(
            room_models.Room,
            number,
            {
                "name": lambda x: seeder.faker.address(),
                "host": lambda x: random.choice(all_users),
                "room_type": lambda x: random.choice(room_types),
                "guests": lambda x: random.randint(1, 5),
                "price": lambda x: random.randint(100, 500),
                "beds": lambda x: random.randint(1, 5),
                "bedrooms": lambda x: random.randint(1, 5),
                "baths": lambda x: random.randint(1, 5),
            },
        )

        # seeder.execute()로 방 생성은 끝났지만 사진이나 시설 등의 정보는 따로 추가해줘야 함
        created_room = seeder.execute()
        print(created_room)
        # get the list of created room's primary key
        created_clean = flatten(list(created_room.values()))
        print(created_clean)

        amenities = room_models.Amenity.objects.all()
        facilities = room_models.Facility.objects.all()
        rules = room_models.HouseRule.objects.all()

        # 만들어진 방에 사진, 옵션, 시설, 룰 추가(생성)
        for pk in created_clean:
            # 만들어진 방을 room 변수에 저장
            room = room_models.Room.objects.get(pk=pk)
            print(room.amenities.all())
            print(room.facilities.all())
            # 사진
            for photo in range(3, random.randint(9, 12)):
                room_models.Photo.objects.create(
                    caption=seeder.faker.sentence(),
                    room=room,
                    file=f"room_photos/{random.randint(1,31)}.webp",
                )
            for amenity in amenities:
                magic_number = random.randint(1, 15)
                if magic_number % 2 == 0:
                    room.amenities.add(amenity)

            for facility in facilities:
                magic_number = random.randint(1, 15)
                if magic_number % 2 == 0:
                    room.facilities.add(facility)

            for rule in rules:
                magic_number = random.randint(1, 15)
                if magic_number % 2 == 0:
                    room.house_rules.add(rule)

        self.stdout.write(self.style.SUCCESS(f"{number} rooms created"))