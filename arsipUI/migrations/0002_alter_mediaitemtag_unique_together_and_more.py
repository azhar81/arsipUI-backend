# Generated by Django 4.2.6 on 2023-10-17 10:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('arsipUI', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='mediaitemtag',
            unique_together=None,
        ),
        migrations.RemoveField(
            model_name='mediaitemtag',
            name='media_item',
        ),
        migrations.RemoveField(
            model_name='mediaitemtag',
            name='tag',
        ),
        migrations.AddField(
            model_name='mediaitem',
            name='tags',
            field=models.ManyToManyField(to='arsipUI.tag'),
        ),
        migrations.DeleteModel(
            name='MediaItemEvent',
        ),
        migrations.DeleteModel(
            name='MediaItemTag',
        ),
    ]