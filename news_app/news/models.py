from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify



class Publication(models.Model):
    author = models.ForeignKey(User, on_delete=models.SET_DEFAULT, default=None, blank=True)
    title = models.CharField(max_length=128, blank=False, unique=True)
    poster_file_name = models.CharField(max_length=32, blank=False, unique=True)
    content = models.TextField(blank=False)
    source_link = models.CharField(max_length=128, blank=False, default=None, unique=True)
    introduction = models.CharField(max_length=64, default=None, blank=True)
    slug = models.SlugField(unique=True, blank=True)
    
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        
        self.introduction = f'{self.content[:64]}...' if len(self.content) > 64 else f'{self.content}...'
        
        super(Publication, self).save(*args, **kwargs)

    def __str__(self):
        return self.title
    
    

class PublicationFile(models.Model):
    file_name = models.CharField(max_length=32, blank=False, unique=True)
    publication = models.ForeignKey(Publication, on_delete=models.CASCADE)

