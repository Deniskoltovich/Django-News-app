# Generated by Django 4.2 on 2023-04-25 20:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0020_alter_publication_slug_alter_publication_source_link_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='publicationfile',
            name='file_name',
            field=models.CharField(max_length=70, unique=True),
        ),
    ]
