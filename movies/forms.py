from django.forms import forms

from movies.models import Reviews
from django.forms import ModelForm

from django import forms


class ReviewForm(forms.ModelForm):
#Для отзывов
    class Meta:
        model = Reviews
        fields = ("name", "email", "text")