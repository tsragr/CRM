import django_filters
from .models import Company
from django_filters import rest_framework as filters


class CompanyFilter(django_filters.FilterSet):

    class Meta:
        model = Company
        fields = {
            'name': ['icontains', 'iexact'],
            'created_at': ['exact', 'gte', 'lte'],
        }
