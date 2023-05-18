FROM nginx:1.21-alpine

RUN rm /etc/nginx/conf.d/default.conf
WORKDIR /home/denis/Django-News-app/news_app/
COPY . .
COPY ./nginx/nginx.conf /etc/nginx/conf.d