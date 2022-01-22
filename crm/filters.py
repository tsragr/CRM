import django_filters
from .models import Company, Office
from django_filters import rest_framework as filters


class CompanyFilter(django_filters.FilterSet):
    offices__count = django_filters.NumberFilter()
    offices__count__gte = django_filters.NumberFilter(field_name='offices__count', lookup_expr='gt')
    offices__count__lte = django_filters.NumberFilter(field_name='offices__count', lookup_expr='lt')

    class Meta:
        model = Company
        fields = {
            'name': ['icontains', 'iexact'],
            'created_at': ['exact', 'gte', 'lte'],
        }


class OfficeFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Office
        fields = ['name', 'company', 'location']
