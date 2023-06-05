from django.db.models import Q
from django.views.generic import ListView, DetailView, TemplateView, View
from django.http import JsonResponse, HttpResponse
from movies.models import Movie, Actor, Genre, Rating
from django.shortcuts import render, redirect

from movies.forms import ReviewForm, RatingForm

from django.db.models import Max, F, Avg


class GenreYear:
#Жанры и года
    def get_genres(self):
        return Genre.objects.all()

    def get_years(self):
        return Movie.objects.filter(draft=False).values("year").order_by("year")


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


class Search(ListView, GenreYear):
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["star_form"] = RatingForm()

        # Получить оценку пользователя для данного фильма (если она существует)
        user_rating = None
        if self.request.user.is_authenticated:
            user_rating = Rating.objects.filter(movie=self.object, ip=self.request.META['REMOTE_ADDR']).first()

        context['user_rating'] = user_rating
        context['average_rating'] = Rating.objects.filter(movie=self.object).aggregate(Avg('star__value'))['star__value__avg']

        return context


class ActorDetailView(DetailView):
    model = Actor
    template_name = 'actor_detail.html'
    slug_field = "name"


class AddStarRating(View):
#добавление рейтинга
    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    def post(self, request):
        form = RatingForm(request.POST)
        if form.is_valid():
            Rating.objects.update_or_create(
                ip=self.get_client_ip(request),
                movie_id=int(request.POST.get("movie")),
                defaults={'star_id': int(request.POST.get("star"))}
            )
            return HttpResponse(status=201)
        else:
            return HttpResponse(status=400)


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