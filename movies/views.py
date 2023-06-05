from django.db.models import Q
from django.views.generic import ListView, DetailView, TemplateView, View
from django.shortcuts import render
from movies.models import Movie, Actor, Genre
from django.shortcuts import render, redirect

from movies.forms import ReviewForm

from django.db.models import Max, F


class GenreYear:
#Жанры и года
    def get_genres(self):
        return Genre.objects.all()

    def get_years(self):
        return Movie.objects.filter(draft=False).values("year")


class NewMoviesListView(ListView):
    model = Movie
    template_name = "main.html"

    def get_new_movie_list(self):
        return Movie.objects.filter(draft=False).annotate(latest_year=Max('genres__movie__year')).\
            filter(year=F('latest_year'))


class MoviesListView(ListView, GenreYear, ):
    model = Movie
    template_name = "movie_list.html"
    queryset = Movie.objects.filter(draft=False)


class InfoView(TemplateView):
    template_name = "inform.html"


class FilterMoviesView(GenreYear, ListView, ):
#Фильтры по фильмам
    template_name = "movie_list.html"
    def get_queryset(self):
        queryset = Movie.objects.filter(
            Q(year__in=self.request.GET.getlist("year")) |
            Q(genres__in=self.request.GET.getlist("genre"))
        ).distinct()
        return queryset


class Search(ListView):
#Поиск по фильму
    #paginate_by = 3
    template_name = "movie_list.html"

    def get_queryset(self):
        return Movie.objects.filter(title__icontains=self.request.GET.get("search"))

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["search"] = f'search={self.request.GET.get("search")}'
        return context


class MovieDetailView(DetailView):
    model = Movie
    template_name = "movie_detail.html"
    slug_field = "url"


class ActorDetailView(DetailView):
    model = Actor
    template_name = 'actor_detail.html'
    slug_field = "name"


class AddReview(View):
#Добавление отзыва
    def post(self, request, pk):
        form = ReviewForm(request.POST)
        movie = Movie.objects.get(id=pk)
        if form.is_valid():
            form = form.save(commit=False)
            if request.POST.get("parent", None):
                form.parent_id = int(request.POST.get("parent"))
            form.movie = movie
            form.save()
        return redirect(movie.get_absolute_url())