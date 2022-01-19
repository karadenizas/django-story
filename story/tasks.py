from celery import shared_task

from django.db.models import Sum


from .models import StoryComment

@shared_task
def expiration_task(story_id, **kwargs):
    qs = StoryComment.objects.filter(story_id=story_id)
    top_rated = qs.filter(rating__rate__isnull=False).annotate(total_rate=Sum('rating__rate')).order_by('-total_rate').first()
    top_rated.attachment = True
    top_rated.save()
    qs.exclude(attachment=True).delete()


@shared_task
def test(x, **kwargs):
    return print(f'this argument is {x}')