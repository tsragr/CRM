from django.urls import path
from rest_framework import routers
from crm import views

router = routers.DefaultRouter()
router.register('company', views.CompanyViewSet, basename='company-list-create')
router.register('detail', views.CompanyDetailViewSet, basename='company-detail')
router.register('cooperation', views.CooperationCreateUpdateViewSet, basename='coop')

urlpatterns = router.urls
