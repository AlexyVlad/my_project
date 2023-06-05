from django.urls import path, include
from movies import views
from movies.views import MoviesListView, MovieDetailView, AddReview, ActorDetailView, FilterMoviesView, \
    NewMoviesListView, InfoView

urlpatterns = [
    path('', NewMoviesListView.as_view(), name="base"),
    path('info', InfoView.as_view(), name="base"),
    path('movies', MoviesListView.as_view(), name="moviesList"),
    path("filter/", views.FilterMoviesView.as_view(), name='filter'),
    path("add-rating/", views.AddStarRating.as_view(), name='add_rating'),
    path("search/", views.Search.as_view(), name='search'),
    path("<slug:slug>/", MovieDetailView.as_view(), name="movie_detail"),
    path("review/<int:pk>/", AddReview.as_view(), name="add_review"),
    path("actor/<str:slug>/", ActorDetailView.as_view(), name="actor_detail"),
]