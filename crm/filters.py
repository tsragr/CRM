import django_filters
from .models import Company
from django_filters import rest_framework as filters


class CompanyFilter(django_filters.FilterSet):
    offices__lte = django_filters.NumberFilter(lookup_expr='lte')
    offices__gte = django_filters.NumberFilter(lookup_expr='gte')

    class Meta:
        model = Company
        fields = {
            'name': ['icontains', 'iexact'],
            'created_at': ['exact', 'gte', 'lte'],
        }
