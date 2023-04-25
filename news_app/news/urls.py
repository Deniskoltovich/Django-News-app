from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


from news.views import (list_publications, publication_details_by_id,
                        publication_details_by_slug, offer_publication, my_news,
                        list_publication_offers, review_publication,
                        edit_rejected_publication, accept_publication)

urlpatterns = [
    path('', list_publications, name='list_publications'),
    path('my_news/offer_publication/', offer_publication, name='offer_publication'),
    path('my_news/', my_news, name = 'my_news'),
    path('my_news/rejected/edit/<int:id>', edit_rejected_publication, name='edit_rejected_publication'),
    path('offers/', list_publication_offers, name='list_publication_offers'),
    path('offers/review/<int:id>/', review_publication, name='review_publication'),
    path('offers/review/<int:id>/accept/', accept_publication, name='accept_publication'),
    path('<int:pub_id>/', publication_details_by_id, name='publication_by_id'),
    path('<slug:pub_slug>/', publication_details_by_slug, name='publication_by_slug'),
]  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
