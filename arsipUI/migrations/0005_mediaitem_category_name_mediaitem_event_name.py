# Generated by Django 4.2.6 on 2023-10-17 10:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('arsipUI', '0004_alter_mediaitem_tags'),
    ]

    operations = [
        migrations.AddField(
            model_name='mediaitem',
            name='category_name',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='mediaitem',
            name='event_name',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
