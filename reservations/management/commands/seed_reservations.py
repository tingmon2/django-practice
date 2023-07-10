import random
from django.core.management.base import BaseCommand  # 내가 만든 core 앱이랑은 관계없는 장고 안의 core임
from django_seed import Seed
from datetime import datetime, timedelta
from reservations import models as reservation_models
from users import models as user_models
from rooms import models as room_models


class Command(BaseCommand):
    help = "create reservations"

    # 몇 명의 유저를 만들 것 인지 지시하기 위해 아규먼트를 더함
    def add_arguments(self, parser):
        parser.add_argument(
            "--number", type=int, default=1, help="How many reservations?"
        )

    # 받아온 숫자만큼 유저를 만드는데 스태프와 관리자가 아니어야 함
    def handle(self, *args, **options):
        number = options.get("number")
        seeder = Seed.seeder()
        users = user_models.User.objects.all()
        rooms = room_models.Room.objects.all()
        seeder.add_entity(
            reservation_models.Reservation,
            number,
            {
                "status": lambda x: random.choice(["pending", "confirmed", "canceled"]),
                "guest": lambda x: random.choice(users),
                "room": lambda x: random.choice(rooms),
                "check_in": lambda x: datetime.now(),
                "check_out": lambda x: datetime.now()
                + timedelta(days=random.randint(1, 24)),
            },
        )
        seeder.execute()
        self.stdout.write(
            self.style.SUCCESS(f"{number} reservationsfrom reservations created")
        )
