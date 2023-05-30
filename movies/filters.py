import django_filters as filters
from movies.models import Movie


class MovieNameFilter(filters.FilterSet):
    name = filters.CharFilter(label="Поиск по названию", field_name='title', lookup_expr="icontains")

    class Meta:
        model = Movie
        fields = ['title', ]