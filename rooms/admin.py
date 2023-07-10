from django.contrib import admin
from django.utils.html import mark_safe
from . import models


# Register your models here.
@admin.register(models.RoomType, models.Facility, models.Amenity, models.HouseRule)
class ItemAdmin(admin.ModelAdmin):
    """Item Admin Definition"""

    list_display = (
        "name",
        "used_by",
    )

    def used_by(self, obj):
        return obj.rooms.count()


# 굳이 포토에 들어가지 않고 방에서 포토를 저장, 수정하기 위해(FK관계로 연결되어 있어야 함)
class PhotoInline(admin.TabularInline):
    model = models.Photo


@admin.register(models.Room)
class RoomAdmin(admin.ModelAdmin):
    """Room Admin Definition"""

    inlines = (PhotoInline,)

    fieldsets = (
        (
            "Basic Info",
            {"fields": ("name", "description", "country", "address", "city", "price")},
        ),
        ("Times", {"fields": ("check_in", "check_out", "instant_book")}),
        ("Place Info", {"fields": ("guests", "beds", "bedrooms", "baths")}),
        (
            "More Info",
            {
                "classes": ("collapse",),
                "fields": ("room_type", "amenities", "facilities", "house_rules"),
            },
        ),
        ("Host", {"fields": ("host",)}),
    )

    ordering = (
        "price",
        "bedrooms",
    )

    list_display = (
        "name",
        "country",
        "city",
        "price",
        "address",
        "guests",
        "beds",
        "bedrooms",
        "baths",
        "instant_book",
        "check_in",
        "check_out",
        "count_amenities",
        "count_photos",
        "total_rating",
    )

    list_filter = (
        "instant_book",
        "host__superhost",
        "host__gender",
        "room_type",
        "amenities",
        "facilities",
        "house_rules",
        "city",
        "country",
    )

    search_fields = ("city", "host__username")

    filter_horizontal = (
        "amenities",
        "facilities",
        "house_rules",
    )

    raw_id_fields = ("host",)  # 이름 대신 아이디 보여주기위해?

    # 어드민에서 세이브를 오버라이드 하는 경우
    # def save_model(self, request, obj, form, change):
    #     # 내가 할 짓 씀 ex) 특정 관리자만 저장 권한을 가짐, 관리자 하나가 정보 저장시 다른 관리자에게 메일 발송 등등
    #     super().save_model(request, obj, form, change)

    # admin속 함수는 어드민 모드에서만 실행하는 함수이고 전체 사이트에 영향 없음
    def count_amenities(self, obj):
        # self는 RoomAdmin 클래스 그자체, obj는 테이블 속 하나의 행(하나의 방 데이터)
        return (
            obj.amenities.count()
        )  # var a = _context.Clubs.Country.FirstOrDefault(x=>x.Country == "Korea").OrderBy(x=>x.CountryCode)

    count_amenities.short_description = "amenities"

    def count_photos(self, obj):
        return obj.photos.count()

    count_photos.short_description = "photo count"


@admin.register(models.Photo)
class PhotoAdmin(admin.ModelAdmin):
    """Photo Admin Definition"""

    list_display = (
        "__str__",
        "get_thumnail",
    )

    def get_thumnail(self, obj):
        # 일반적으로 장고는 억지로 집어넣은 코드는 실행안함(보안상의 이유로)
        # mark_safe는 개발자가 이것은 의도한 것이니까 실행하라는 의미
        return mark_safe(f'<img width="50px" src="{obj.file.url}"/>')

    get_thumnail.short_description = "Thumnail"
