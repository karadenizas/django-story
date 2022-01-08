# Generated by Django 4.0 on 2022-01-04 20:37

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('story', '0014_alter_story_expiration_alter_storycomment_expiration_and_more'),
    ]

    operations = [
        migrations.RemoveIndex(
            model_name='story',
            name='story_story_draft_9138f2_idx',
        ),
        migrations.AlterField(
            model_name='story',
            name='completed',
            field=models.BooleanField(db_index=True, default=False),
        ),
        migrations.AlterField(
            model_name='story',
            name='draft',
            field=models.BooleanField(db_index=True, default=True),
        ),
        migrations.AlterField(
            model_name='story',
            name='expiration',
            field=models.DateTimeField(default=datetime.datetime(2022, 1, 5, 20, 37, 19, 81526, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='storycomment',
            name='expiration',
            field=models.DateTimeField(default=datetime.datetime(2022, 1, 5, 20, 37, 19, 82115, tzinfo=utc)),
        ),
    ]
