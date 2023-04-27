import datetime as dt

from django.test import TestCase, Client
from django.urls import reverse
from news.models import Publication
from django.contrib.auth.models import User


class TestView(TestCase):
    
    fixtures = ['users.json']
    
    def setUp(self) -> None:
        self.client = Client()
        self.user = User.objects.get(username='admin')
        return super().setUp()
    
    
    def test_publication_list_GET(self):
        response = self.client.get(reverse('list_publications'))
        
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'list_news.html')
      
        
    def test_publication_details_slug_GET(self):        
        
        Publication.objects.create(
            author=self.user,
            title='срочная новость',
            content='Some content',
            poster_file_name='some_name.jpg',  
        )
        response = self.client.get(reverse('publication_by_slug', args=('breaking-news',)))
        
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'publication_details.html')
        
        
    def test_accept_user_publication_by_admin(self):
        pub = Publication.objects.create(
            author=self.user,
            title='срочная новость',
            content='Some content',
            poster_file_name='some_name.jpg',
            status=Publication.Status.REVIEWING
        )
        
        self.client.login(username='admin', password='admin')
        response = self.client.get(reverse('accept_publication', args=(pub.id,)))
        
        self.assertEquals(response.status_code, 302)
      
        
    def test_accept_user_publication_by_user(self):
        pub = Publication.objects.create(
            author=self.user,
            title='срочная новость',
            content='Some content',
            poster_file_name='some_name.jpg',
            status=Publication.Status.REVIEWING
        )
        
        self.client.login(username='sample_user', password='user1234')
        response = self.client.get(reverse('accept_publication', args=(pub.id,)))
        
        self.assertEquals(response.status_code, 403)
        
    
        
    def test_login_required_my_news_page(self):
        response = self.client.get(reverse('my_news'))
        self.assertEquals(response.status_code, 302)
        self.assertTemplateNotUsed(response, 'offer_menu.html')

        
        self.client.login(username='sample_user', password='user1234')
        response = self.client.get(reverse('my_news'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'offer_menu.html')


    def test_admin_required_list_offers_page(self):
        self.client.login(username='sample_user', password='user1234')
        response = self.client.get(reverse('list_publication_offers'))
        self.assertEquals(response.status_code, 403)
        self.assertTemplateNotUsed(response, 'admin_menu.html')

        
        self.client.login(username='admin', password='admin')
        response = self.client.get(reverse('list_publication_offers'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'admin_menu.html')
        
        
    def test_admin_required_review_page(self):
        pub = Publication.objects.create(
            author=self.user,
            title='срочная новость',
            content='Some content',
            poster_file_name='some_name.jpg',
            status=Publication.Status.REVIEWING
        )
        
        self.client.login(username='sample_user', password='user1234')
        response = self.client.get(reverse('review_publication', args=(pub.id,)))
        self.assertEquals(response.status_code, 403)
        self.assertTemplateNotUsed(response, 'review_page.html')

        
        self.client.login(username='admin', password='admin')
        response = self.client.get(reverse('review_publication', args=(pub.id,)))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'review_page.html')
        
        
    def test_login_required_offer_publication(self):
        response = self.client.get(reverse('offer_publication'))
        self.assertEquals(response.status_code, 302)
        self.assertTemplateNotUsed(response, 'offer_publication.html')

        
        self.client.login(username='sample_user', password='user1234')
        response = self.client.get(reverse('offer_publication'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'offer_publication.html')
        