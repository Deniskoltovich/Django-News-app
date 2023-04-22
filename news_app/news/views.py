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
    publications = Publication.objects.filter(status=Publication.Status.ACCEPTED)
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
            publication.status = Publication.Status.REVIEWING
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
    

@login_required        
def my_news(request):
    user_publications = Publication.objects.filter(author=request.user)
    accepted_user_publications = user_publications.filter(status=Publication.Status.ACCEPTED)
    rejected_user_publications = user_publications.filter(status=Publication.Status.REJECTED)
    
    context = {
        'offered_publications': user_publications,
        'accepted_publications': accepted_user_publications,
        'rejected_publications': rejected_user_publications,
        'are_offers_exist': user_publications.count() > 0,
    }
    return render(request, 'offer_menu.html', context)

@login_required
def list_publication_offers(request):
    pending_rewiew_publications = Publication.objects.filter(status=Publication.Status.REVIEWING)
    rejected_publications = Publication.objects.filter(status=Publication.Status.REJECTED)
    
    context = {
        'has_pending_review': pending_rewiew_publications.count() > 0,
        'are_rejected_exist': rejected_publications.count() > 0,
        'pending_rewiew_publications': pending_rewiew_publications,
        'rejected_publications': rejected_publications
    }
    
    return render(request, 'admin_menu.html', context)
    