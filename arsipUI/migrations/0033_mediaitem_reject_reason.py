# Generated by Django 4.2.6 on 2023-12-11 03:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('arsipUI', '0032_remove_file_media_item_mediaitem_file_paths'),
    ]

    operations = [
        migrations.AddField(
            model_name='mediaitem',
            name='reject_reason',
            field=models.TextField(default='', editable=False),
        ),
    ]
