# Generated by Django 4.2.6 on 2023-12-04 12:11

import arsipUI.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('arsipUI', '0027_mediaitem_verificator_alter_mediaitem_contributor'),
    ]

    operations = [
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to=arsipUI.models.media_file_path)),
            ],
        ),
        migrations.RemoveField(
            model_name='mediaitem',
            name='file_path',
        ),
        migrations.AddField(
            model_name='mediaitem',
            name='file_path',
            field=models.ManyToManyField(related_name='media_items', to='arsipUI.file'),
        ),
    ]