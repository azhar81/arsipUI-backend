# Generated by Django 4.2.6 on 2023-11-09 09:55

import arsipUI.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('arsipUI', '0008_alter_mediaitem_tags'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mediaitem',
            name='file_path',
            field=models.FileField(upload_to=arsipUI.models.media_file_path),
        ),
    ]
