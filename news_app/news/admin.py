from django.contrib import admin

from news.models import Publication, PublicationFile, RejectedPublication

admin.site.register(Publication)
admin.site.register(PublicationFile)
admin.site.register(RejectedPublication)