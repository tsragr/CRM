from django.urls import path
from rest_framework import routers
from crm import views

router = routers.DefaultRouter()
router.register('company', views.CompanyViewSet)
router.register('company-detail', views.CompanyDetailViewSet)
router.register('office', views.ListOfficeViewSet)

urlpatterns = router.urls
