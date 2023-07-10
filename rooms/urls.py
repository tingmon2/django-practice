from django.urls import path
from . import views

app_name = "rooms"
# [path("argument", module(views).function, name="detail")]
urlpatterns = [
    path("<int:pk>", views.RoomDetail.as_view(), name="detail"),
    path("search/", views.SearchView.as_view(), name="search"),
]
