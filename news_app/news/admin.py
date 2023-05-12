import os, glob

from typing import Any
from django.core.files.storage import FileSystemStorage
from django.contrib import admin
from django.db.models.query import QuerySet
from django.http.request import HttpRequest

from settings.base import BASE_DIR


from news.models import Publication, PublicationFile, RejectedPublication

class PublicationAdmin(admin.ModelAdmin):
    actions = ['delete_selected',]
    
    def delete_queryset(self, request: HttpRequest, queryset: QuerySet[Any]) -> None:
        fss = FileSystemStorage()
        static_dir = os.path.join(BASE_DIR, 'news/static/')

        for publication in queryset:
            fss.delete(f'{static_dir}/posters/{publication.poster_file_name}')
            for image in glob.glob(f'{static_dir}/images/*{publication.poster_file_name}'):
                fss.delete(image)
            publication.delete()
            

admin.site.register(Publication, PublicationAdmin)
admin.site.register(PublicationFile)
admin.site.register(RejectedPublication)