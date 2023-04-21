import os

from googletrans import Translator
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseNotFound
from news.models import Publication, PublicationFile
from news.forms import NewsCreationForm
from settings.base import BASE_DIR


def list_publications(request):
    publications = Publication.objects.filter(accepted_by_admin=True)
    context = {
        'title': 'News',
        'publications': publications,
    }
    return render(request, 'list_news.html', context=context)
    
def publication_details_by_id(request, pub_id: int):
    try:
        publication = Publication.objects.get(pk=pub_id)
    except Publication.DoesNotExist:
        return HttpResponseNotFound(('Publication does not exist'))

    return redirect('publication_details_by_slug', publication.slug)


def publication_details_by_slug(request, pub_slug: str):
    try:
        publication = Publication.objects.get(slug=pub_slug)
    except Publication.DoesNotExist:
        return HttpResponseNotFound(('Publication does not exist'))
    
    publication_files = PublicationFile.objects.filter(publication=publication)

    context = {
        'title': publication.title,
        'publication': publication,
        'publication_files': publication_files
    }
    return render(request, 'publication_details.html', context=context)
    

@login_required()
def upload(request):
    if request.method == 'POST':
        news_form = NewsCreationForm(request.POST)
        if news_form.is_valid():
            publication_title_eng = Translator().translate(news_form.cleaned_data['title']).text
            publication_title_eng = publication_title_eng.replace('"','').replace("'", '').replace(' ', '_')[:60]
            posters_dir = os.path.join(BASE_DIR, f'news/static/posters/{publication_title_eng}')
            
            upload = request.FILES['poster_upload']
            fss = FileSystemStorage()
            file = fss.save(posters_dir + '.jpg', upload)
            
            publication = news_form.save(commit=False)
            publication.author = request.user
            publication.poster_file_name = publication_title_eng + '.jpg'
            publication.accepted_by_admin = False
            publication.save()
            context = {
                'title': publication.title,
                'publication': publication,
            }
            return render(request, 'publication_details.html', context=context)
        
    else:
        news_form = NewsCreationForm()
        
    context = {
        'form': news_form
    }
    return render(request, 'offer_publication.html', context)
        

