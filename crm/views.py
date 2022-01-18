from django.shortcuts import render
from django.shortcuts import get_object_or_404
from rest_framework import generics, mixins, viewsets
from .serializers import CompanySerializer, CompanyDetailSerializer, CompanyCreateSerializers, OfficeSerializer, \
    OfficesCompanySerializer, CreateOfficeCompanySerializer
from .models import Company, Office, Worker
from django_filters.rest_framework import DjangoFilterBackend
from .filters import CompanyFilter, OfficeFilter
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from rest_framework.decorators import action
from rest_framework.response import Response


class CompanyViewSet(viewsets.GenericViewSet,
                     mixins.ListModelMixin,
                     mixins.CreateModelMixin):
    queryset = Company.objects.filter(is_active=True)
    filter_backends = [DjangoFilterBackend]
    filterset_class = CompanyFilter
    serializers = {'list': CompanySerializer,
                   'create': CompanyCreateSerializers}

    def get_serializer_class(self):
        return self.serializers[self.action]


"""
    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]
"""


class CompanyDetailViewSet(viewsets.GenericViewSet,
                           mixins.RetrieveModelMixin,
                           mixins.UpdateModelMixin,
                           mixins.DestroyModelMixin, ):
    queryset = Company.objects.all()
    filter_backends = [DjangoFilterBackend]
    serializers = {'retrieve': CompanyDetailSerializer,
                   'partial_update': CompanyCreateSerializers,
                   'update': CompanyCreateSerializers,
                   'create_office_company': CreateOfficeCompanySerializer
                   }

    def get_serializer_class(self):
        return self.serializers[self.action]

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()

    @action(detail=True)
    def companies_offices(self, request, pk=None):
        queryset = Office.objects.filter(company__id=pk)
        serializer = OfficesCompanySerializer(queryset, many=True)
        return Response(serializer.data)

    @action(methods=['post'], detail=True)
    def create_office_company(self, request, pk=None):
        serializer = self.serializers[self.action](data=request.data)
        if serializer.is_valid():
            office = serializer.save()
            office.company = get_object_or_404(Company, pk=pk)
            office.save()
        return Response(serializer.data)


"""
    def get_permissions(self):
        if self.action == 'retrieve':
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]
"""


class ListOfficeViewSet(viewsets.GenericViewSet,
                        mixins.ListModelMixin):
    filter_backends = [DjangoFilterBackend]
    filterset_class = OfficeFilter
    queryset = Office.objects.all()
    serializer_class = OfficeSerializer
