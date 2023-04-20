import os

from bs4 import BeautifulSoup
from django.contrib.auth.models import User
import requests
import urllib.request
from googletrans import Translator

from news.models import Publication, PublicationFile
from news_app import celery_app
from settings.base import BASE_DIR  


def download_image(url: str, dir_name: str, file_name: str):
    urllib.request.urlretrieve(url, os.path.join(BASE_DIR, f"news/static/{dir_name}/{file_name}"))
    

def scrape_ria_publication(url: str):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    pubication_title = soup.find('div', {'class': 'article__title'}).text
    publication_title_eng = Translator().translate(pubication_title).text
    
    content_body = soup.find('div', {'class': 'article__body'})
    publication_content = ''
    for text_block in content_body.find_all('div', {'class': 'article__text'}):
        publication_content += text_block.text
    
    admin = User.objects.get(pk=1)

    publication = Publication.objects.create(
        author = admin,
        title = pubication_title,
        content = publication_content,
        source_link = url,
        poster_file_name = f'{publication_title_eng}.jpg'
    )
    return publication
    

@celery_app.task(bind=True)
def scrape_news_from_ria_ru(request):
    
    response = requests.get('https://ria.ru/world/')
    soup = BeautifulSoup(response.text, 'html.parser')
    content_block = soup.find('div', {'class': 'list list-tags'})
    for news_item in content_block.find_all('div', {'class': 'list-item'}):
        publication_href = news_item.find('div',{'class': 'list-item__content'} ).find('a')['href']
        
        publication = scrape_ria_publication(publication_href)
        poster_href = news_item.find('div',{'class': 'list-item__content'} )\
            .find('a', {'class':'list-item__image'})\
            .find('picture')\
            .find('source')['srcset']
            
        download_image(poster_href, 'posters', publication.poster_file_name)
        
                
