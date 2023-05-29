from django.views.generic import ListView, DetailView, View
from django.shortcuts import render
from movies.models import Movie
from django.shortcuts import render, redirect
from .forms import ReviewForm


def index(request):
    return render(request, 'main.html')


class MoviesListView(ListView):
    model = Movie
    template_name = "movie_list.html"


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