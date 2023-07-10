from django.core.management.base import BaseCommand  # 내가 만든 core 앱이랑은 관계없는 장고 안의 core임
from rooms.models import Facility


class Command(BaseCommand):
    # def add_arguments(self, parser):
    #     parser.add_argument("--times", help="How many times?")

    help = "create facilities"

    def handle(self, *args, **options):
        facilities = [
            "Private entrance",
            "Paid parking on premises",
            "Paid parking off premises",
            "Elevator",
            "Parking",
            "Gym",
        ]
        for item in facilities:
            Facility.objects.create(name=item)
        self.stdout.write(self.style.SUCCESS("facilities created"))
