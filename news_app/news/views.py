from django.shortcuts import render, redirect
from django.http import HttpResponseNotFound
from news.models import Publication, PublicationFile


def list_publications(request):
    publications = Publication.objects.all()
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

    context = {
        'title': publication.title,
        'pub': publication,
    }
    return render(request, 'publication_details.html', context=context)
    


