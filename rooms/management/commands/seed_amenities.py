from django.core.management.base import BaseCommand  # 내가 만든 core 앱이랑은 관계없는 장고 안의 core임
from rooms.models import Amenity


class Command(BaseCommand):
    # def add_arguments(self, parser):
    #     parser.add_argument("--times", help="How many times?")

    help = "create amenities"

    def handle(self, *args, **options):
        amenities = [
            "Kitchen",
            "Heating",
            "Washer",
            "Wifi",
            "Indoor fireplace",
            "Iron",
            "Laptop friendly workspace",
            "Crib",
            "Self check-in",
            "Carbon monoxide detector",
            "Shampoo",
            "Air conditioning",
            "Dryer",
            "Breakfast",
            "Hangers",
            "Hair dryer",
            "TV",
            "High chair",
            "Smoke detector",
            "Private bathroom",
        ]
        for item in amenities:
            Amenity.objects.create(name=item)
        self.stdout.write(self.style.SUCCESS("Amenities created"))