from django import forms
from . import models


class LoginForm(forms.Form):

    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    # "clean_"은 validation 역할의 함수에 항상 붙여야하는 법칙(선택X 강제) ex)clean_password
    def clean(self):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        try:
            user = models.User.objects.get(username=email)
            if user.check_password(password):
                print(password)
                return self.cleaned_data
            else:
                self.add_error("password", forms.ValidationError("Incorrect password"))
        except models.User.DoesNotExist:
            self.add_error("email", forms.ValidationError("User does not exist"))


class SignUpForm(forms.ModelForm):
    class Meta:
        model = models.User
        fields = ("first_name", "last_name", "email")

    password = forms.CharField(widget=forms.PasswordInput)
    password1 = forms.CharField(widget=forms.PasswordInput, label="Password Confirm")

    def clean_password1(self):
        password = self.cleaned_data.get("password")
        password1 = self.cleaned_data.get("password1")
        if password != password1:
            raise forms.ValidationError("passwords are not same")
        else:
            return password

    # override save method
    def save(self, *args, **kwargs):
        try:
            username = self.cleaned_data.get("email")
            password = self.cleaned_data.get("password")
            # commit=False는 오브젝트는 만들되 데이터 베이스에 저장은 하지 말라는 뜻. 디폴트는 당연히 트루
            user = super().save(commit=False)
            user.username = username
            user.set_password(password)
            # 그냥 저장은 commit=True임
            user.save()
        except Exception:
            raise forms.ValidationError("email is already being used")


# without ModelForm -> have to manually create fields
# class SignUpForm(forms.Form):
#     first_name = forms.CharField(max_length=15)
#     last_name = forms.CharField(max_length=15)
#     email = forms.EmailField()
#     password = forms.CharField(widget=forms.PasswordInput)
#     password1 = forms.CharField(widget=forms.PasswordInput, label="Password Confirm")

#     def clean_email(self):
#         email = self.cleaned_data.get("email")
#         try:
#             models.User.objects.get(email=email)
#             raise forms.ValidationError("email is already being used")
#         except models.User.DoesNotExist:
#             return email

#     # 필드를 순차적으로 불러오기 때문에 clean_password 라고 함수를 만들면 password1이 사용불가임
#     def clean_password1(self):
#         password = self.cleaned_data.get("password")
#         password1 = self.cleaned_data.get("password1")
#         if password != password1:
#             raise forms.ValidationError("passwords are not same")
#         else:
#             return password

#     def save(self):
#         first_name = self.cleaned_data.get("first_name")
#         last_name = self.cleaned_data.get("last_name")
#         email = self.cleaned_data.get("email")
#         password = self.cleaned_data.get("password")

#         user = models.User.objects.create_user(email, email, password)
#         user.first_name = first_name
#         user.last_name = last_name
#         user.save()