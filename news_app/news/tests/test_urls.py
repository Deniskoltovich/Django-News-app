from django.test import SimpleTestCase
from django.urls import reverse, resolve

from news.views import *


class TestUrls(SimpleTestCase):
    def test_list_publications_url_resolves(self):
        url = reverse('list_publications')
        self.assertEquals(resolve(url).func, list_publications)
        
    def test_publication_details_by_id_url_resolves(self):
        url = reverse('publication_by_id', args=(1,))
        self.assertEquals(resolve(url).func, publication_details_by_id)
        
    def test_publication_details_by_slug_url_resolve(self):
        url = reverse('publication_by_slug', args=('hello-world',))
        self.assertEquals(resolve(url).func, publication_details_by_slug)
        
    def test_offer_publication_url_resolves(self):
        url = reverse('offer_publication')
        self.assertEquals(resolve(url).func, offer_publication)
        
    def test_my_news_url_resolves(self):
        url = reverse('my_news')
        self.assertEquals(resolve(url).func, my_news)
        
    def test_list_publication_offers_url_resolve(self):
        url = reverse('list_publication_offers')
        self.assertEquals(resolve(url).func, list_publication_offers)
        
        
    def test_accept_publication_url_resolves(self):
        url = reverse('accept_publication', args=(1,))
        self.assertEquals(resolve(url).func, accept_publication)

    def test_review_publication_url_resolves(self):
        url = reverse('review_publication', args=(1,))
        self.assertEquals(resolve(url).func, review_publication)
        
    def test_edit_rejected_publication_resolve(self):
        url = reverse('edit_rejected_publication', args=(1,))
        self.assertEquals(resolve(url).func, edit_rejected_publication)
        
    