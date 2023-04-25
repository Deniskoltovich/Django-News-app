from googletrans import Translator

from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify


class Publication(models.Model):
    
    class Status(models.TextChoices):
        ACCEPTED = 'Accepted'
        REJECTED = 'Rejected'
        REVIEWING = 'Reviewing'
        
        
    author = models.ForeignKey(User, on_delete=models.SET_DEFAULT, default=None, blank=True)
    title = models.CharField(max_length=255, blank=False, unique=True)
    poster_file_name = models.CharField(max_length=64, blank=False, unique=True)
    content = models.TextField(blank=False, max_length=5120)
    source_link = models.CharField(max_length=255, default=None, null=True)
    introduction = models.CharField(max_length=64, default=None, blank=True)
    time_created = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=9, choices=Status.choices, default=Status.ACCEPTED)
    slug = models.SlugField(unique=True, blank=True, max_length=255)
    
    class Meta:
        ordering = ['-time_created']
        indexes = [
            models.Index(fields=['title',]),
        ]

    
    
    def save(self, *args, **kwargs):
        """Custom save method with slug creation using google translator API and intoduction field filling"""
        if not self.slug:
            title_translation = Translator().translate(self.title).text
            self.slug = slugify(title_translation)
        
        self.introduction = f'{self.content[:61]}...' if len(self.content) > 61 else f'{self.content}...'
        
        super(Publication, self).save(*args, **kwargs)

    def __str__(self):
        return self.title
    
    
class RejectedPublication(models.Model):
    reason_for_rejection = models.TextField(blank=False, null=False)
    publication = models.ForeignKey(Publication, on_delete=models.CASCADE)
    
    class Meta:
        indexes = [
            models.Index(fields=['publication',]),
        ]
        
    def __str__(self):
        return self.reason_for_rejection


class PublicationFile(models.Model):
    file_name = models.CharField(max_length=70, blank=False, unique=True)
    publication = models.ForeignKey(Publication, on_delete=models.CASCADE)

