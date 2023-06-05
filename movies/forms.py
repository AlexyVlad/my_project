from django.forms import forms

from movies.models import Reviews, Rating, RatingStar
from django.forms import ModelForm

from django import forms


class ReviewForm(forms.ModelForm):
#Для отзывов
    class Meta:
        model = Reviews
        fields = ("name", "email", "text")


class RatingForm(forms.ModelForm):
#добавить рейтинг
    star = forms.ModelChoiceField(
        queryset=RatingStar.objects.all(), widget=forms.RadioSelect(), empty_label=None
    )

    class Meta:
        model = Rating
        fields = ("star",)

