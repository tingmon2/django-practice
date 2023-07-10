import random
from django.core.management.base import BaseCommand  # 내가 만든 core 앱이랑은 관계없는 장고 안의 core임
from django_seed import Seed
from django.contrib.admin.utils import flatten
from lists import models as list_models
from users import models as user_models
from rooms import models as room_models


class Command(BaseCommand):
    help = "create lists"

    # 몇 명의 유저를 만들 것 인지 지시하기 위해 아규먼트를 더함
    def add_arguments(self, parser):
        parser.add_argument("--number", type=int, default=1, help="How many lists?")

    # 받아온 숫자만큼 유저를 만드는데 스태프와 관리자가 아니어야 함
    def handle(self, *args, **options):
        number = options.get("number")
        seeder = Seed.seeder()
        users = user_models.User.objects.all()
        rooms = room_models.Room.objects.all()
        seeder.add_entity(
            list_models.List,
            number,
            {
                "user": lambda x: random.choice(users),
            },
        )
        created = seeder.execute()
        cleaned = flatten(list(created.values()))
        for pk in cleaned:
            list_model = list_models.List.objects.get(pk=pk)
            # 리스트 형태인 rooms에서 랜덤 범위[a : b](a와 b사이)만큼 뽑아서 리스트로 만듦
            to_add = rooms[random.randint(0, 5) : random.randint(6, 30)]
            # *를 붙이는 이유는 리스트 자체가 아니라 그 안의 값들을 갖고 싶기 때문
            list_model.rooms.add(*to_add)
        self.stdout.write(self.style.SUCCESS(f"{number} lists created"))