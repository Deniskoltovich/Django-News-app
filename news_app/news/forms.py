from django.forms import ModelForm

from news.models import Publication

class NewsCreationForm(ModelForm):
    """ Form for creation Publication instance"""
    class Meta:
        model = Publication
        exclude = [ 'source_link', 'creation_date', 'poster_file_name', 'accepted_by_admin', 'introduction', 'slug', 'author', 'status']

    def __init__(self, *args, **kwargs):
        super(NewsCreationForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
            
