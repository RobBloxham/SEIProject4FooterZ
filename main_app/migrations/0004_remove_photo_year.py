# Generated by Django 3.1.2 on 2020-10-12 17:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0003_photo_year'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='photo',
            name='year',
        ),
    ]
