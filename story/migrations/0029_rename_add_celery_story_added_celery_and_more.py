# Generated by Django 4.0.1 on 2022-01-17 14:09

import datetime
import django.core.validators
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('story', '0028_story_add_celery_alter_story_expiration_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='story',
            old_name='add_celery',
            new_name='added_celery',
        ),
        migrations.AlterField(
            model_name='story',
            name='expiration',
            field=models.DateTimeField(default=datetime.datetime(2022, 1, 18, 14, 9, 9, 528383, tzinfo=utc), validators=[django.core.validators.MinValueValidator(datetime.datetime(2022, 1, 17, 14, 9, 9, 528391, tzinfo=utc)), django.core.validators.MaxValueValidator(datetime.datetime(2022, 1, 18, 14, 9, 9, 528396, tzinfo=utc))]),
        ),
        migrations.AlterField(
            model_name='storycomment',
            name='expiration',
            field=models.DateTimeField(default=datetime.datetime(2022, 1, 18, 14, 9, 9, 529024, tzinfo=utc)),
        ),
    ]