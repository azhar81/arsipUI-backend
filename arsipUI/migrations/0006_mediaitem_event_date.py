# Generated by Django 4.2.6 on 2023-10-17 10:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('arsipUI', '0005_mediaitem_category_name_mediaitem_event_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='mediaitem',
            name='event_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
