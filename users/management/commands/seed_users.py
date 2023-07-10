from django.core.management.base import BaseCommand  # 내가 만든 core 앱이랑은 관계없는 장고 안의 core임
from django_seed import Seed
from users.models import User


class Command(BaseCommand):
    help = "create users"

    # 몇 명의 유저를 만들 것 인지 지시하기 위해 아규먼트를 더함
    def add_arguments(self, parser):
        parser.add_argument("--number", type=int, default=1, help="How many users?")

    # 받아온 숫자만큼 유저를 만드는데 스태프와 관리자가 아니어야 함
    def handle(self, *args, **options):
        number = options.get("number")
        seeder = Seed.seeder()
        seeder.add_entity(User, number, {"is_staff": False, "is_superuser": False})
        seeder.execute()
        self.stdout.write(self.style.SUCCESS(f"{number} users created"))