# Generated by Django 4.2 on 2023-04-25 19:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0013_rejectedpublication'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='publication',
            index=models.Index(fields=['title'], name='news_public_title_2a8af3_idx'),
        ),
        migrations.AddIndex(
            model_name='rejectedpublication',
            index=models.Index(fields=['publication'], name='news_reject_publica_43309f_idx'),
        ),
    ]
