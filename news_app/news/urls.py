from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


from news.views import list_publications, publication_details_by_id, publication_details_by_slug

urlpatterns = [
    path('', list_publications, name='list_publications'),
    path('<int:pub_id>/', publication_details_by_id, name='publication_by_id'),
    path('<slug:pub_slug>/', publication_details_by_slug, name='publication_by_slug'),
]  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
