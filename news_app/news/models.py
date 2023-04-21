from googletrans import Translator

from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify

#TODO поставить четкие границы блоков в publication_details

class Publication(models.Model):
    author = models.ForeignKey(User, on_delete=models.SET_DEFAULT, default=None, blank=True)
    title = models.CharField(max_length=128, blank=False, unique=True)
    poster_file_name = models.CharField(max_length=64, blank=False, unique=True)
    content = models.TextField(blank=False)
    source_link = models.CharField(max_length=128, default=None, null=True)
    introduction = models.CharField(max_length=64, default=None, blank=True)
    time_created = models.DateTimeField(auto_now_add=True)
    accepted_by_admin = models.BooleanField(default=True) 
    slug = models.SlugField(unique=True, blank=True)
    
    class Meta:
        ordering = ['-time_created']

    
    
    def save(self, *args, **kwargs):
        """Custom save method with slug creation using google translator API and intoduction field filling"""
        if not self.slug:
            title_translation = Translator().translate(self.title).text
            self.slug = slugify(title_translation)
        
        self.introduction = f'{self.content[:61]}...' if len(self.content) > 61 else f'{self.content}...'
        
        super(Publication, self).save(*args, **kwargs)

    def __str__(self):
        return self.title
    
    

class PublicationFile(models.Model):
    file_name = models.CharField(max_length=32, blank=False, unique=True)
    publication = models.ForeignKey(Publication, on_delete=models.CASCADE)

