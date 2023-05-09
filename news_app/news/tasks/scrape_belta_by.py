"""
Module with
"""

import requests
from bs4 import BeautifulSoup
from django.contrib.auth.models import User
from news.models import Publication, PublicationFile
from news.tasks.scrape_ria_ru import download_image

from news_app import celery_app

headers = {
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36 OPR/97.0.0.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'DNT': '1',
    'Accept-Encoding': 'gzip, deflate, lzma, sdch',
    'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.6,en;q=0.4'
}


def scrape_images(content_body, poster_file_name: str, publication: Publication) -> list:
    """
    Finds all images in CONTENT_BODY, saves this images and links them with PUBLICATION
    :param content_body: HTML tag that contains images
    :param poster_file_name: filename to save
    :param publication: Publication object to connect with files
    :return: list of PUBLICATION's files
    """
    publication_files = []
    for index, image in enumerate(content_body.find_all('img')):
        try:
            try:
                publication_image_href = image['src']
            except KeyError:
                publication_image_href = image['alt title src']
        except KeyError:
            publication_image_href = image['data-src']

        try:
            download_image(publication_image_href, 'images', f'{index}_{poster_file_name}.jpg')
        except ValueError:
            download_image('https://www.belta.by' + publication_image_href, 'images', f'{index}_{poster_file_name}.jpg')

        publication_files.append(PublicationFile(file_name=f'{index}_{poster_file_name}.jpg', publication=publication))

    return publication_files


def scrape_belta_publication(url: str) -> tuple[Publication, list[PublicationFile]] or tuple[None, None]:
    """
    Processes page creating Publication instance and it's files
    :param url: publication's url
    :return: Tuple(<Publication object>, list[PublicationFile] )  or (None, None) in case if publication already exists
    """
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    publication_title = soup.find('div', {'class': 'main'}).find('div', {'class': 'content_2_col'})
    try:
        publication_title = publication_title.find('div', {'class': 'content_margin'}).find('h1').text
    except AttributeError:
        publication_title = publication_title.find('div', {'class': 'content_2_col_margin'}).find('h1').text

    try:
        content_body = soup.find('div', {'class': 'content_margin'}).find('div', {'class': 'js-mediator-article'})
    except AttributeError:
        content_body = soup.find('div', {'class': 'content_2_col_margin'}).find('div', {'class': 'js-mediator-article'})

    if Publication.objects.filter(title=publication_title).count() != 0:
        return None, None

    publication_content = ''
    for text_block in content_body.find_all('p'):
        publication_content += f'{text_block.text}\n\n'

    admin = User.objects.get(pk=1)

    poster_file_name = ''
    for char in publication_title[:60]:
        if char == ' ':
            poster_file_name += '_'
        elif char.isalpha():
            poster_file_name += char

    publication = Publication.objects.create(
        author=admin,
        title=publication_title,
        content=publication_content,
        source_link=url,
        poster_file_name=poster_file_name + '.jpg'
    )

    publication_files = []

    try:
        main_image = content_body.findParent('div', {'class': 'text'}).find('div', {'class': 'main_img'}).find(
            'picture').find('img')
        download_image(main_image['src'], 'images', f'{poster_file_name}.jpg')
        publication_files.append(PublicationFile(file_name=f'{poster_file_name}.jpg', publication=publication))
    except AttributeError:
        pass

    publication_files.extend(scrape_images(content_body, poster_file_name, publication))

    return publication, publication_files


@celery_app.task(bind=True)
def scrape_news_from_belta_by(request):
    """
    Main scraping function that finds all publications on the https://www.belta.by/all_news page
    and calls scrape_belta_publication() for each publication
    """
    response = requests.get('https://www.belta.by/all_news', headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    content_block = soup.find('div', {'class': 'content'}).find('div', {'class': 'lenta_inner'})
    publications = []
    publications_files = []
    for news_item in content_block.find_all('div', {'class': 'news_item lenta_item'}):
        try:
            poster_href = news_item.find('span', {'class': 'lenta_img'}).find('img')['src']
        except AttributeError:
            continue
        title = news_item.find('span', {'class': 'lenta_item_title'}).text
        publication_href = news_item.find('a', {'title': title})['href']
        publication, publication_files = scrape_belta_publication('https://www.belta.by' + publication_href)
        if publication is None:
            continue
        publications_files.extend(publication_files)
        download_image(poster_href, 'posters', publication.poster_file_name)

    PublicationFile.objects.bulk_create(publications_files)
