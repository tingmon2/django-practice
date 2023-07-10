from django.urls import path
from rooms import views as room_views

# 홈페이지, 로그인 등 가장 기본 화면을 보여줌

app_name = "core"

urlpatterns = [
    path("", room_views.HomeView.as_view(), name="home"),
]
