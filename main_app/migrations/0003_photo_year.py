# Generated by Django 3.1.2 on 2020-10-12 17:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0002_auto_20201012_0007'),
    ]

    operations = [
        migrations.AddField(
            model_name='photo',
            name='year',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
