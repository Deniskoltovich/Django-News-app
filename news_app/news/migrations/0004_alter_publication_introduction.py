# Generated by Django 4.2 on 2023-04-19 22:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0003_alter_publication_introduction_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='publication',
            name='introduction',
            field=models.CharField(blank=True, default=None, max_length=64),
        ),
    ]