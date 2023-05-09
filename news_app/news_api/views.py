from django.shortcuts import render
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters



from news.models import Publication
from news_api.serializers import PublicationSerializer


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 5

    def get_paginated_response(self, data):
        return Response({
            'has_next': self.page.has_next(),
            'has_prev': self.page.has_previous(),
            'count': self.page.paginator.count,
            'results': data
        })



class PublicationViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Publication.objects.all().order_by()
    serializer_class = PublicationSerializer
    filter_backends = [
       DjangoFilterBackend, filters.SearchFilter,
       filters.OrderingFilter]
    filterset_fields = ['source_link']
    search_fields = ['title', 'content']
    ordering_fields = ['time_created',]
    ordering = ['-time_created']
    pagination_class = StandardResultsSetPagination
