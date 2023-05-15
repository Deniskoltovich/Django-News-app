import datetime as dt

from django.test import TestCase
from django.contrib.auth.models import User
from django.db.utils import IntegrityError

from news.models import Publication, PublicationFile


class TstModels(TestCase):
    fixtures = ['users.json']
    
    def setUp(self) -> None:
        self.user = User.objects.get(username='admin')
        self.publication1 = Publication.objects.create(
            author=self.user,
            title='срочная новость',
            content='Some content',
            poster_file_name='some_name.jpg',  
        )
        self.publication_file1 = PublicationFile.objects.create(
            publication = self.publication1,
            file_name = 'some_file.jpg'
        )
        
        return super().setUp()
    
    def test_publication_is_assigned_slug_on_creation(self):
        self.assertEquals(self.publication1.slug, 'breaking-news')
        
        
    def test_publication_is_assigned_introduction_on_creation(self):
        self.assertEquals(self.publication1.introduction, "Some content...")
    
    
    def test_publication_is_assigned_default_status_on_creation(self):
        self.assertEquals(self.publication1.status, Publication.Status.ACCEPTED)
        
        
    def test_unique_publication_slug(self):
        with self.assertRaises(IntegrityError):
            event2 = Publication.objects.create(
                author=self.user,
                title='срочная новость',
                content='Some content',
                poster_file_name='some_name2.jpg',  
            )
            
    def test_unique_publication_title(self):
        with self.assertRaises(IntegrityError):
            event2 = Publication.objects.create(
                author=self.user,
                title='срочная новость2',
                content='Some content',
                poster_file_name='some_name.jpg',  
            )
         
         
            
    def test_unique_publication_poster_filename(self):
        with self.assertRaises(IntegrityError):
            event2 = Publication.objects.create(
                author=self.user,
                title='срочная новость2',
                content='Some content',
                poster_file_name='some_name.jpg',  
            )
            
    def test_unique_publciation_file_filename(self):
        with self.assertRaises(IntegrityError):
            PublicationFile.objects.create(
                publication = self.publication1,
                file_name = 'some_file.jpg'
            )
            
    
    
        
    