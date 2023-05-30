from django.views.generic import ListView, DetailView, View
from django.shortcuts import render
from movies.models import Movie
from django.shortcuts import render, redirect

from . import filters
from .forms import ReviewForm


def index(request):
    return render(request, 'main.html')


class MoviesListView(ListView):
    model = Movie
    template_name = "movie_list.html"

    def get_filters(self):
        return filters.MovieNameFilter(self.request.GET)

    def get_queryset(self):
        return self.get_filters().qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = self.get_filters()
        return context


class MovieDetailView(DetailView):
    model = Movie
    #slug_field = "url"
    template_name = "movie_detail.html"


class AddReview(View):
    """Отзывы"""
    def post(self, request, pk):
        form = ReviewForm(request.POST)
        movie = Movie.objects.get(id=pk)
        if form.is_valid():
            form = form.save(commit=False)
            form.movie = movie
            form.save()
        return redirect("/movies/"+str(pk))