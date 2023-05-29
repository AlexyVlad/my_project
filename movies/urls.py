from django.urls import path, include
from . import views
from .views import MoviesListView, MovieDetailView

urlpatterns = [
    path('', views.index, name="base"),
    path('movies', MoviesListView.as_view(), name="moviesList"),
    path('movies/<int:pk>', MovieDetailView.as_view(), name="detail_movie"),
    path("review/<int:pk>/", views.AddReview.as_view(), name="add_review"),
]