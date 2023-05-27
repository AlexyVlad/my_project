from django.views.generic import ListView
from django.shortcuts import render
from movies.models import Movie


def index(request):
    return render(request, 'main.html')


class MoviesListView(ListView):
    model = Movie
    template_name = "movies.html"


