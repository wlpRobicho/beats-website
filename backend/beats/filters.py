import django_filters
from django_filters import DurationFilter
from .models import Beat

class BeatFilter(django_filters.FilterSet):
    genre = django_filters.CharFilter(field_name='genre', lookup_expr='iexact')
    key = django_filters.CharFilter(field_name='key', lookup_expr='iexact')
    tag = django_filters.CharFilter(method='filter_by_tag')
    is_featured = django_filters.BooleanFilter()
    bpm = django_filters.NumberFilter()
    bpm__gte = django_filters.NumberFilter(field_name='bpm', lookup_expr='gte')
    bpm__lte = django_filters.NumberFilter(field_name='bpm', lookup_expr='lte')
    duration__gte = DurationFilter(field_name='duration', lookup_expr='gte')
    duration__lte = DurationFilter(field_name='duration', lookup_expr='lte')

    class Meta:
        model = Beat
        fields = ['genre', 'key', 'bpm', 'is_featured']

    def filter_by_tag(self, queryset, name, value):
        return queryset.filter(tags__icontains=value)
