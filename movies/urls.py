from django.urls import path, include
from . import views
from .views import MoviesListView

urlpatterns = [
    path('', views.index, name="base"),
    path('movies', MoviesListView.as_view(), name="moviesList"),
]