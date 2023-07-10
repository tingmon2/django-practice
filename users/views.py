from django.shortcuts import render, redirect, reverse
from django.urls import (
    reverse_lazy,
)  # same as reverse but does not call url automatically
from django.views import View
from django.views.generic import FormView
from django.contrib.auth import authenticate, login, logout
from . import forms, models


class LoginView(FormView):
    template_name = "users/login.html"
    form_class = forms.LoginForm
    success_url = reverse_lazy("core:home")
    initial = {"email": "tingmon2@gmail.com"}

    # if form is valid,
    def form_valid(self, form):
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, username=email, password=password)
        if user is not None:
            login(self.request, user)
        return super().form_valid(form)  # goes to success_url


def log_out(request):
    logout(request)
    return redirect(reverse("core:home"))


class SignUpView(FormView):
    template_name = "users/signup.html"
    form_class = forms.SignUpForm
    success_url = reverse_lazy("core:home")
    initial = {
        "first_name": "Thomas",
        "last_name": "Aquinas",
        "email": "tingmon@naver.com",
    }

    def form_valid(self, form):
        form.save()
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, username=email, password=password)
        if user is not None:
            login(self.request, user)
        user.verify_email()
        return super().form_valid(form)


def complete_verification(request, secret):
    try:
        print(secret)
        user = models.User.objects.get(email_secret=secret)
        user.email_verified = True
        user.save()
    except models.User.DoesNotExist:
        pass
    return redirect(reverse("core:home"))


# without FormView
# class LoginView(View):
#     # 처음 페이지가 열렸을 떄
#     def get(self, request):
#         form = forms.LoginForm(initial={"email": "asdf@asdf.com"})
#         return render(request, "users/login.html", {"form": form})

#     # 유저가 입력한 값을 제출했을 떄
#     def post(self, request):
#         form = forms.LoginForm(request.POST)
#         # forms.py에 있는 clean 함수가 먼저 실행됨
#         if form.is_valid():
#             email = form.cleaned_data.get("email")
#             password = form.cleaned_data.get("password")
#             user = authenticate(request, username=email, password=password)
#             if user is not None:
#                 login(request, user)
#                 return redirect(reverse("core:home"))
#         return render(request, "users/login.html", {"form": form})

# 클래스 기반 뷰에서 겟과 포스트 함수를 부르는 것과 동일
# def login_view(request):
#     if request.method == "GET"
#         pass
#     elif request.method == "POST"