from django.shortcuts import render, redirect, reverse
from django.core.paginator import Paginator, EmptyPage
from django.views.generic import ListView, DetailView, View
from django.utils import timezone
from django.http import Http404
from django_countries import countries
from math import ceil
from . import models, forms

# from django.http import HttpResponse

# Create your views here.
class HomeView(ListView):

    """Homeview Definition"""

    model = models.Room
    # ListView의 어트리뷰트를 통해 훨씬 쉽게 아래의 페이지들을 만듦
    paginate_by = 10
    paginate_orphans = 5
    page_kwarg = "page"  # keyward argument
    ordering = "created"
    context_object_name = "rooms"

    # c#의 _context같은 존재에 어트리뷰트 추가
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     now = timezone.now()
    #     context["now"] = now
    #     return context


class RoomDetail(DetailView):

    """RoomDetail Definition"""

    # html에서 해당 방의 정보를 room.name 처럼 쓸 수 있음 왜냐면 장고가 알아서 모델명을 인식함
    # 혹은 그냥 object.name 으로 쓸 수 있음 (즉, function base 처럼 room = models.Room.objects.get(pk=pk) 필요X)
    model = models.Room
    print(model)


class SearchView(View):
    def get(self, request):
        country = request.GET.get("country")
        rooms = None

        if country:
            # 들어온 정보를 검증하고 기억
            form = forms.SearchForm(request.GET)
            # 폼에 에러가 없다면
            if form.is_valid():
                city = form.cleaned_data.get("city")
                country = form.cleaned_data.get("country")
                room_type = form.cleaned_data.get("room_type")
                price = form.cleaned_data.get("price")
                guests = form.cleaned_data.get("guests")
                bedrooms = form.cleaned_data.get("bedrooms")
                beds = form.cleaned_data.get("beds")
                baths = form.cleaned_data.get("baths")
                instant_book = form.cleaned_data.get("instant_book")
                superhost = form.cleaned_data.get("superhost")
                amenities = form.cleaned_data.get("amenities")
                facilities = form.cleaned_data.get("facilities")

                filter_args = {}
                # filter_args["검색항목(모델에서 주어진 이름)__검색조건"] = 검색항목
                if city != "Anywhere" or city == "":
                    filter_args["city__startswith"] = city
                filter_args["country"] = country
                if room_type is not None:
                    filter_args["room_type"] = room_type
                if price is not None:
                    filter_args["price__lte"] = price
                if guests is not None:
                    filter_args["guests__gte"] = guests
                if bedrooms is not None:
                    filter_args["bedrooms__gte"] = bedrooms
                if beds is not None:
                    filter_args["beds__gte"] = beds
                if baths is not None:
                    filter_args["baths__gte"] = baths
                if instant_book is True:
                    filter_args["instant_book"] = True
                if superhost is True:
                    filter_args["host__superhost"] = True

                for amenity in amenities:
                    filter_args["amenities"] = amenity

                for facility in facilities:
                    filter_args["facilities"] = facility

                print(filter_args)

                qs = models.Room.objects.filter(**filter_args).order_by("created")

                print(qs)

                paginator = Paginator(qs, 10, orphans=5)

                page = request.GET.get("page", 1)

                rooms = paginator.get_page(page)

                return render(
                    request, "rooms/search.html", {"form": form, "rooms": rooms}
                )

        else:
            # 서치폼이 처음 열린 상태로 아무 입력값이 없기 때문에 validation 안함
            form = forms.SearchForm()

        return render(request, "rooms/search.html", {"form": form})


# with form API based on fucntion
# def search(request):
#     # 패러미터 request.GET이 제출한 폼의 내용을 기억함(unbound form -> bound form)
#     # 이제 데이터와 폼이 연결되었으므로 자동으로 validation 함
#     country = request.GET.get("country")
#     rooms = None

#     if country:
#         # 들어온 정보를 검증하고 기억
#         form = forms.SearchForm(request.GET)
#         # 폼에 에러가 없다면
#         if form.is_valid():
#             city = form.cleaned_data.get("city")
#             country = form.cleaned_data.get("country")
#             room_type = form.cleaned_data.get("room_type")
#             price = form.cleaned_data.get("price")
#             guest = form.cleaned_data.get("guest")
#             bedrooms = form.cleaned_data.get("bedrooms")
#             beds = form.cleaned_data.get("beds")
#             baths = form.cleaned_data.get("baths")
#             instant_book = form.cleaned_data.get("instant_book")
#             superhost = form.cleaned_data.get("superhost")
#             amenities = form.cleaned_data.get("amenities")
#             facilities = form.cleaned_data.get("facilities")

#             filter_args = {}
#             # filter_args["검색항목(모델에서 주어진 이름)__검색조건"] = 검색항목
#             if city != "Anywhere" or city == "":
#                 filter_args["city__startswith"] = city
#             filter_args["country"] = country
#             if room_type is not None:
#                 filter_args["room_type"] = room_type
#             if price is not None:
#                 filter_args["price__lte"] = price
#             if guest is not None:
#                 filter_args["guest__gte"] = guest
#             if bedrooms is not None:
#                 filter_args["bedrooms__gte"] = bedrooms
#             if beds is not None:
#                 filter_args["beds__gte"] = beds
#             if baths is not None:
#                 filter_args["baths__gte"] = baths
#             if instant_book is True:
#                 filter_args["instant_book"] = True
#             if superhost is True:
#                 filter_args["host__superhost"] = True

#             for amenity in amenities:
#                 filter_args["amenities"] = amenity

#             for facility in facilities:
#                 filter_args["facilities"] = facility

#             print(filter_args)

#             rooms = models.Room.objects.filter(**filter_args)

#     else:
#         # 서치폼이 처음 열린 상태로 아무 입력값이 없기 때문에 validation 안함
#         form = forms.SearchForm()

#     return render(request, "rooms/search.html", {"form": form, "rooms": rooms})


# without django form API
# def search(request):
#     # http://127.0.0.1:8000/rooms/search/?city=asdf 이 주소에서 city의 값을 물어옴
#     city = request.GET.get("city", "Anywhere")
#     city = str.capitalize(city)
#     # print(city)
#     country = request.GET.get("country", "KR")
#     room_type = int(request.GET.get("room_type", 0))
#     price = int(request.GET.get("price", 0))
#     guest = int(request.GET.get("guest", 0))
#     bedrooms = int(request.GET.get("bedrooms", 0))
#     beds = int(request.GET.get("beds", 0))
#     baths = int(request.GET.get("baths", 0))
#     instant = bool(request.GET.get("instant", False))
#     superhost = bool(request.GET.get("superhost", False))
#     s_amenities = request.GET.getlist("amenities")
#     s_facilities = request.GET.getlist("facilities")

#     print(instant, superhost)

#     form = {
#         # form으로 제출된 url주소에 있는 값들을 관리 + 선택, 입력된 정보를 제출 후에도 폼에서 유지(s_)
#         "city": city,
#         "selected_room_type": room_type,
#         "selected_country": country,
#         "price": price,
#         "guest": guest,
#         "bedrooms": bedrooms,
#         "beds": beds,
#         "baths": baths,
#         "s_amenities": s_amenities,
#         "s_facilities": s_facilities,
#         "instant": instant,
#         "superhost": superhost,
#     }

#     room_types = models.RoomType.objects.all()
#     amenities = models.Amenity.objects.all()
#     facilities = models.Facility.objects.all()

#     choices = {
#         # 데이터베이스에 있는 모델을 보여주기 위해
#         "countries": countries,
#         "room_types": room_types,
#         "amenities": amenities,
#         "facilities": facilities,
#     }

#     filter_args = {}
#     # filter_args["검색항목(모델에서 주어진 이름)__검색조건"] = 검색항목
#     if city != "Anywhere" or city == "":
#         filter_args["city__startswith"] = city
#     filter_args["country"] = country
#     if room_type != 0:
#         filter_args["room_type__pk"] = room_type
#     if price != 0:
#         filter_args["price__lte"] = price
#     if guest != 0:
#         filter_args["guest__gte"] = guest
#     if bedrooms != 0:
#         filter_args["bedrooms__gte"] = bedrooms
#     if beds != 0:
#         filter_args["beds__gte"] = beds
#     if baths != 0:
#         filter_args["baths__gte"] = baths
#     if instant is True:
#         filter_args["instant_book"] = True
#     if superhost is True:
#         filter_args["host__superhost"] = True

#     if len(s_amenities) > 0:
#         for s_amenitiy in s_amenities:
#             filter_args["amenities__pk"] = int(s_amenitiy)
#     if len(s_facilities) > 0:
#         for s_facility in s_facilities:
#             filter_args["facilities__pk"] = int(s_facility)

#     print(filter_args)

#     rooms = models.Room.objects.filter(**filter_args)

#     return render(
#         request,
#         "rooms/search.html",
#         # **는 현재 딕셔너리를 풀어내겠다는 뜻
#         context={**form, **choices, "rooms": rooms},
#     )


# function base detail page
# def room_detail(request, pk):
#     try:
#         room = models.Room.objects.get(pk=pk)
#     except models.Room.DoesNotExist:
#         raise Http404()

#     return render(
#         request,
#         "rooms/detail.html",
#         {"room": room},
#     )


# with paginator
# def all_rooms(request):
#     # 디폴트가 1인 페이지 /?page=1
#     page = request.GET.get("page", 1)
#     room_list = models.Room.objects.all()
#     # paginator는 리스트와 페이지 당 요소 갯수, 5이하로 넘치는 요소는 마지막 페이지에 같이 넣음
#     paginator = Paginator(room_list, 10, orphans=4)
#     try:
#         rooms = paginator.page(int(page))
#         return render(
#             request,
#             "rooms/home.html",
#             {"page": rooms},
#         )
#     except EmptyPage:
#         rooms = paginator.page(1)
#         return redirect("/")


# without paginator
# def all_rooms(request):
#     # 디폴트가 1인 페이지 /?page=1
#     page = request.GET.get("page", 1)
#     # /?page= 같이 페이지 값이 없을 경우 방지
#     page = int(page or 1)
#     page_size = 10
#     limit = page_size * page
#     offset = limit - page_size
#     # [a:b] a에서 b까지의 엘리먼트들을 보여줘라
#     all_rooms = models.Room.objects.all()[offset:limit]
#     page_count = ceil(models.Room.objects.count() / page_size)
#     return render(
#         request,
#         "rooms/home.html",
#         context={
#             "rooms": all_rooms,
#             "page": page,
#             "page_count": page_count,
#             "page_range": range(0, page_count),
#         },
#     )