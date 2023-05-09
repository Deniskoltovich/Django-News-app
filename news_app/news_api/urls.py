from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PublicationViewSet

router = DefaultRouter()
router.register(r'', PublicationViewSet)


urlpatterns = [
    path('', include(router.urls)),
]
