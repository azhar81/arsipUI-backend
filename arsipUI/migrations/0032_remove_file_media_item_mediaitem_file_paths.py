# Generated by Django 4.2.6 on 2023-12-05 11:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('arsipUI', '0031_remove_mediaitem_file_paths_file_media_item_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='file',
            name='media_item',
        ),
        migrations.AddField(
            model_name='mediaitem',
            name='file_paths',
            field=models.ManyToManyField(related_name='media_items', to='arsipUI.file'),
        ),
    ]