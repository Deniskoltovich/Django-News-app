import os
import urllib.request

import requests
from bs4 import BeautifulSoup
from django.contrib.auth.models import User
from news.models import Publication, PublicationFile
from settings.base import BASE_DIR
from googletrans import Translator


from news_app import celery_app


def download_image(url: str, dir_name: str, file_name: str) -> None:
    """
    :param url: Image's url
    :param dir_name: dir to save
    :param file_name: new image's filename
    :return: None
    """
    img_path = os.path.join(BASE_DIR, f"news/static/{dir_name}/{file_name}")
    urllib.request.urlretrieve(url, img_path)
    print(os.path.abspath(img_path))


def scrape_ria_publication(url: str) -> tuple[Publication, PublicationFile] or tuple[None, None]:
    """
       Processes page creating Publication instance and it's main image
       :param url: publication's url
       :return: Tuple(<Publication object>, PublicationFile) or (None, None) in case if publication already exists
    """

    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    try:
        publication_title = soup.find('div', {'class': 'article__title'}).text
    except AttributeError:
        publication_title = soup.find('h1', {'class': 'article__title'}).text

    if Publication.objects.filter(title=publication_title).count() != 0:
        return None, None

    content_body = soup.find('div', {'class': 'article__body'})
    publication_content = ''
    for text_block in content_body.find_all('div', {'class': 'article__text'}):
        publication_content += f'{text_block.text}\n\n'

    admin = User.objects.get(pk=1)
    poster_file_name = ''
    for char in Translator().translate(publication_title).text[:60]:
        if char == ' ':
            poster_file_name += '_'
        elif char.isalpha():
            poster_file_name += char
            
    
    try:
        publication_image_href = soup.find('div', {'class': 'article__header'}).find('img')['src']
    except (TypeError, AttributeError):
        return None, None
    publication = Publication.objects.create(
        author=admin,
        title=publication_title,
        content=publication_content,
        source_link=url,
        poster_file_name=poster_file_name + '.jpg'
    )

    download_image(publication_image_href, 'images', f'{poster_file_name}.jpg')

    return publication, PublicationFile(file_name=f'{poster_file_name}.jpg', publication=publication)


@celery_app.task(bind=True)
def scrape_news_from_ria_ru(request) -> None:
    """
    Main scraping function that finds all publications on the https://ria.ru/world/ page
    and calls scrape_ria_publication() for each publication
    """
    response = requests.get('https://ria.ru/world/')
    soup = BeautifulSoup(response.text, 'html.parser')
    content_block = soup.find('div', {'class': 'list list-tags'})

    publications_files = []
    for news_item in content_block.find_all('div', {'class': 'list-item'}):
        publication_href = news_item.find('div', {'class': 'list-item__content'}).find('a')['href']
        publication, publication_file = scrape_ria_publication(publication_href)

        if publication is None: continue

        poster_href = news_item.find('div', {'class': 'list-item__content'}) \
            .find('a', {'class': 'list-item__image'}) \
            .find('picture') \
            .find('source')['srcset']

        publications_files.append(publication_file)
        download_image(poster_href, 'posters', publication.poster_file_name)

    PublicationFile.objects.bulk_create(publications_files)
