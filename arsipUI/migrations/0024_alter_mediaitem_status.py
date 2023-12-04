# Generated by Django 4.2.6 on 2023-12-03 09:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('arsipUI', '0023_event_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mediaitem',
            name='status',
            field=models.CharField(choices=[('waitlist', 'Waitlist'), ('approved', 'Approved'), ('rejected', 'Rejected')], editable=False, max_length=8),
        ),
    ]