# Generated by Django 4.0.1 on 2022-01-10 11:59

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('story', '0020_rating_rate_alter_story_expiration_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='commentrating',
            name='rate',
        ),
        migrations.AlterField(
            model_name='story',
            name='expiration',
            field=models.DateTimeField(default=datetime.datetime(2022, 1, 11, 11, 59, 46, 990780, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='storycomment',
            name='expiration',
            field=models.DateTimeField(default=datetime.datetime(2022, 1, 11, 11, 59, 46, 991526, tzinfo=utc)),
        ),
    ]