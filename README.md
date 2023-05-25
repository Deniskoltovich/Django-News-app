# Django-News-app
News aggregator application

The following were performed:

-parsing web pages with beautiful soup 4;

-scraping news articles with Celery tasks, scheduled by Celery beat;

-creating an API;

-Dockerizing project with Nginx to serve static and media.

## Quick start
With docker:

```
docker-compose -f news_app/docker-compose.prod.yaml up --build  
```
