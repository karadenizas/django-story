# Generated by Django 4.0.1 on 2022-01-10 11:58

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('story', '0018_alter_story_expiration_alter_storycomment_expiration'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='rating',
            name='rate',
        ),
        migrations.AlterField(
            model_name='story',
            name='expiration',
            field=models.DateTimeField(default=datetime.datetime(2022, 1, 11, 11, 58, 32, 889742, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='storycomment',
            name='expiration',
            field=models.DateTimeField(default=datetime.datetime(2022, 1, 11, 11, 58, 32, 890376, tzinfo=utc)),
        ),
    ]
