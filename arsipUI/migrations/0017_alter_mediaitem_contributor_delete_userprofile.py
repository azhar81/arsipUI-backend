# Generated by Django 4.2.6 on 2023-11-30 12:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
        ('arsipUI', '0016_userprofile_mediaitem_contributor'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mediaitem',
            name='contributor',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='users.userprofile'),
        ),
        migrations.DeleteModel(
            name='UserProfile',
        ),
    ]