from django import forms
from django_countries.fields import CountryField
from . import models

# 장고의 form API를 이용해 html코딩 줄이기
# 변수이름은 모델에서와 동일하게
class SearchForm(forms.Form):
    city = forms.CharField(initial="Anywhere")
    country = CountryField(default="KR").formfield()
    room_type = forms.ModelChoiceField(
        required=False, empty_label="Any Type", queryset=models.RoomType.objects.all()
    )
    price = forms.IntegerField(required=False)
    guest = forms.IntegerField(required=False, max_value=5)
    bedrooms = forms.IntegerField(required=False, max_value=5)
    beds = forms.IntegerField(required=False, max_value=5)
    baths = forms.IntegerField(required=False, max_value=5)
    instant_book = forms.BooleanField(required=False)
    superhost = forms.BooleanField(required=False)
    amenities = forms.ModelMultipleChoiceField(
        queryset=models.Amenity.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )
    facilities = forms.ModelMultipleChoiceField(
        queryset=models.Facility.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )
