from rest_framework import serializers


from news.models import Publication


class PublicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publication 
        exclude = ['introduction', 'status', 'poster_file_name']
        
