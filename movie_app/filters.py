from django_filters import FilterSet
from .models import Country, Genre, Movie, Actor


class CountryFilter(FilterSet):
    class Meta:
        model = Country
        fields = {
            'country_name': ['exact']
        }


class GenreFilter(FilterSet):
    class Meta:
        model = Genre
        fields = {
            'genre_name': ['exact']
        }


class MovieFilter(FilterSet):
    class Meta:
        model = Movie
        fields = {
            'status': ['exact'],
            'country': ['exact']
        }


class ActorFilter(FilterSet):
    class Meta:
        model = Actor
        fields = {
            'full_name': ['exact']
        }
