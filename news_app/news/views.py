import os
from datetime import datetime

from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.files.storage import FileSystemStorage
from django.db import transaction
from django.db.models import Q
from django.http import HttpResponseNotFound, HttpResponse, HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from news.forms import NewsCreationForm
from news.models import Publication, PublicationFile, RejectedPublication
from settings.base import BASE_DIR


def list_publications(request) -> HttpResponse:
    """
    Render 'list_news.html 'page with all publications
    or with filtered publications if query params are given
    :return:  HttpResponse
    """
    publications = Publication.objects.filter(status=Publication.Status.ACCEPTED)
    query_params = request.GET
    if query_params:
        date = query_params.get('date')
        content_to_search = query_params.get('search')
        source = query_params.get('source')
        if date:
            date = datetime.strptime(date, '%Y-%d-%m').date()
            publications = Publication.objects.filter(time_created__date=date)
        elif content_to_search:
            publications = Publication.objects.filter(Q(title__contains=content_to_search)
                                                      | Q(content__contains=content_to_search))
        elif source:
            publications = Publication.objects.filter(source_link__contains=source)

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


def publication_details_by_slug(request, pub_slug: str) -> HttpResponse:
    """
    Tries to find Publication by given slug and renders page with its details
    """
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
@transaction.atomic()
def offer_publication(request):
    """
    Create user publication if request method is 'POST' or render page with Publication creation form otherwise
    """
    if request.method == 'POST':
        news_form = NewsCreationForm(request.POST)
        if news_form.is_valid():
            poster_file_name = ''
            for char in news_form.cleaned_data['title'][:60]:
                if char == ' ':
                    poster_file_name += '_'
                elif char.isalnum():
                    poster_file_name += char

            static_dir = os.path.join(BASE_DIR, 'news/static/')

            upload = request.FILES['poster_upload']
            fss = FileSystemStorage()
            fss.save(f'{static_dir}/posters/{poster_file_name}.jpg', upload)
            fss.save(f'{static_dir}/images/{poster_file_name}.jpg', upload)

            publication = news_form.save(commit=False)
            publication.author = request.user
            publication.poster_file_name = poster_file_name + '.jpg'
            publication.status = Publication.Status.REVIEWING
            publication.save()

            PublicationFile.objects.create(file_name=f'{poster_file_name}.jpg',
                                           publication=publication)

            return redirect('publication_by_slug', publication.slug)

    else:
        news_form = NewsCreationForm()

    context = {
        'form': news_form
    }
    return render(request, 'offer_publication.html', context)


@login_required
def my_news(request):
    """ Render page with menu to manage publications offered by user """
    user_publications = Publication.objects.filter(author=request.user)
    offered_publications = user_publications.filter(status=Publication.Status.REVIEWING)
    accepted_user_publications = user_publications.filter(status=Publication.Status.ACCEPTED)
    rejected_user_publications = user_publications.filter(status=Publication.Status.REJECTED)

    context = {
        'offered_publications': offered_publications,
        'accepted_publications': accepted_user_publications,
        'rejected_publications': rejected_user_publications,
        'are_offers_exist': offered_publications.count() > 0,
    }
    return render(request, 'offer_menu.html', context)


@login_required
def list_publication_offers(request):
    """
    ONLY for superuser. Render page with all publications offers created by users
    """
    if not request.user.is_superuser:
        return HttpResponseForbidden()

    pending_rewiew_publications = Publication.objects.filter(status=Publication.Status.REVIEWING)
    rejected_publications = Publication.objects.filter(status=Publication.Status.REJECTED)

    context = {
        'has_pending_review': pending_rewiew_publications.count() > 0,
        'are_rejected_exist': rejected_publications.count() > 0,
        'pending_rewiew_publications': pending_rewiew_publications,
        'rejected_publications': rejected_publications
    }
    return render(request, 'admin_menu.html', context)


@login_required
@transaction.atomic()
def edit_rejected_publication(request, id):
    """
    Edit user's offered publication after admin's review
    :param id: Publication id
    """
    publication = get_object_or_404(Publication, pk=id)
    reasons_for_rejection = RejectedPublication.objects.filter(publication=publication)

    if request.method == 'POST':
        form = NewsCreationForm(request.POST, instance=publication)
        if form.is_valid():
            poster_file_name = ''
            for char in form.cleaned_data['title'][:60]:
                if char == ' ':
                    poster_file_name += '_'
                elif char.isalnum():
                    poster_file_name += char

            static_dir = os.path.join(BASE_DIR, 'news/static/')
            PublicationFile.objects.filter(publication=publication).delete()
            upload = request.FILES['poster_upload']
            fss = FileSystemStorage()
            fss.delete(f'{static_dir}/posters/{publication.poster_file_name}')
            fss.delete(f'{static_dir}/images/{publication.poster_file_name}')
            fss.save(f'{static_dir}/posters/{poster_file_name}.jpg', upload)
            fss.save(f'{static_dir}/images/{poster_file_name}.jpg', upload)

            publication = form.save(commit=False)
            # publication.author = request.user
            publication.poster_file_name = poster_file_name + '.jpg'
            publication.status = Publication.Status.REVIEWING
            publication.save()

            PublicationFile.objects.create(file_name=f'{poster_file_name}.jpg',
                                           publication=publication)

            return redirect('publication_by_slug', publication.slug)

    else:
        form = NewsCreationForm(instance=publication)
    context = {
        'form': form,
        'reasons_for_rejection': reasons_for_rejection
    }
    return render(request, 'edit_publication.html', context)


@login_required
@transaction.atomic()
def review_publication(request, id: int):
    """
    ONLY for superuser. Render the page with offered publication to review
    :param id: Publication id
    """
    if not request.user.is_superuser:
        return HttpResponseForbidden()

    publication_for_review = get_object_or_404(Publication, pk=id)
    publication_files = PublicationFile.objects.filter(publication=publication_for_review)
    if request.method == 'POST':
        reason_for_rejection = request.POST['reason_for_rejection']
        RejectedPublication.objects.create(
            publication=publication_for_review,
            reason_for_rejection=reason_for_rejection
        )

        publication_for_review.status = Publication.Status.REJECTED
        publication_for_review.save()

        return redirect('list_publication_offers')
    else:
        context = {
            'title': publication_for_review.title,
            'publication': publication_for_review,
            'publication_files': publication_files
        }
        return render(request, 'review_page.html', context)


@login_required
def accept_publication(request, id: int):
    """
    ONLY for superuser. Accept publication created by user
    :param id: Publication id
    """
    if request.user.is_superuser:
        publication = get_object_or_404(Publication, pk=id)
        publication.status = Publication.Status.ACCEPTED
        publication.save()

        return redirect('list_publication_offers')
    
    return HttpResponseForbidden()
