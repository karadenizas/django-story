# Generated by Django 4.0 on 2022-01-02 15:48

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('story', '0011_character_comment_alter_story_expiration_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='character',
            name='story',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='character', to='story.story'),
        ),
        migrations.AlterField(
            model_name='story',
            name='expiration',
            field=models.DateTimeField(default=datetime.datetime(2022, 1, 3, 15, 48, 29, 912194, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='storycomment',
            name='expiration',
            field=models.DateTimeField(default=datetime.datetime(2022, 1, 3, 15, 48, 29, 912759, tzinfo=utc)),
        ),
    ]
