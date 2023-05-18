from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PublicationViewSet
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
    openapi.Info(title='News API', default_version='v1'))

router = DefaultRouter()
router.register(r'', PublicationViewSet)


urlpatterns = [
    path('doc/', schema_view.with_ui()),
    path('', include(router.urls)),
]
