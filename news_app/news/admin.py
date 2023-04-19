from django.contrib import admin

from news.models import Publication, PublicationFile

admin.site.register(Publication)
admin.site.register(PublicationFile)