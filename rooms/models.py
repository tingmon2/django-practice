from django.db import models
from django.urls import reverse
from django_countries.fields import CountryField
from core import models as core_models

# from users import models as user_models


class AbstractItem(core_models.TimeStampedModel):

    """Abstract Item """

    name = models.CharField(max_length=80)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class RoomType(AbstractItem):

    """ RoomType Model Definition """

    # 어드민 패널 룸 모델 항목들에 이름지정, 자동으로 뒤에 s붙여줌
    class Meta:
        verbose_name = "Room Type"
        ordering = ["name"]


class Amenity(AbstractItem):
    """ Amenity Model Definition """

    # 그냥 두면 장고가 어드민 패널에서 자동으로 Amenitys로 하기 때문
    class Meta:
        verbose_name_plural = "Amenities"


class Facility(AbstractItem):
    """ Facility Model Definition """

    class Meta:
        verbose_name_plural = "Facilities"


class HouseRule(AbstractItem):
    """ HouseRule Model Definition """

    class Meta:
        verbose_name = "House Rule"


class Photo(core_models.TimeStampedModel):
    """Photo Model Definition"""

    caption = models.CharField(max_length=80)
    file = models.ImageField(upload_to="room_photos")
    room = models.ForeignKey("Room", related_name="photos", on_delete=models.CASCADE)

    def __str__(self):
        return self.caption


# Create your models here.
class Room(core_models.TimeStampedModel):

    """Room Model Definition"""

    name = models.CharField(max_length=100)
    description = models.TextField()
    country = CountryField()
    city = models.CharField(max_length=80)
    price = models.IntegerField()
    address = models.CharField(max_length=140)
    guests = models.IntegerField()
    beds = models.IntegerField()
    bedrooms = models.IntegerField()
    baths = models.IntegerField()
    check_in = models.TimeField()
    check_out = models.TimeField()
    instant_book = models.BooleanField(default=False)
    host = models.ForeignKey(
        "users.User", related_name="rooms", on_delete=models.CASCADE
    )  # related_name => 유저쪽에서 방을 찾을 때 사용할 이름
    room_type = models.ForeignKey(
        "RoomType", related_name="rooms", on_delete=models.SET_NULL, null=True
    )  # 외부키로 연결된 테이블은 서로를 볼 수 있음
    amenities = models.ManyToManyField("Amenity", related_name="rooms", blank=True)
    facilities = models.ManyToManyField("Facility", related_name="rooms", blank=True)
    house_rules = models.ManyToManyField("HouseRule", related_name="rooms", blank=True)

    def __str__(self):
        return self.name

    # 메소드 오버라이딩(앞으로 이 모델을 저장 할 때 마다 어디서든 이 함수가 실행됨)
    def save(self, *args, **kwargs):
        self.city = str.capitalize(self.city)  # 저장전 데이터를 인터셉트해서 수정함
        super().save(*args, **kwargs)

    # admin panel에서 데이터베이스의 방정보를 view로 보여줄 때를 위한 오버라이드 (view on site 버튼)
    def get_absolute_url(self):
        return reverse("rooms:detail", kwargs={"pk": self.pk})

    # 평균 레이팅은 향후 프런트엔드에서도 쓸 것이기 때문에 어드민이 아닌 모델에 함수를 선언함
    def total_rating(self):
        all_reviews = self.reviews.all()
        all_ratings = 0
        for review in all_reviews:
            all_ratings += review.rating_average()
        if all_reviews.count() == 0:
            return 0
        else:
            return round(all_ratings / len(all_reviews), ndigits=1)
