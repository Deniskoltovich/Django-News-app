# Generated by Django 4.2 on 2023-04-25 20:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0018_alter_publicationfile_file_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='publication',
            name='source_link',
            field=models.CharField(default=None, max_length=256, null=True),
        ),
    ]