from django import template
from django.db.models import Count

from ..models import Rating, CommentRating, Story

register = template.Library()

@register.filter
def get_comment_rate(value, arg):
    return CommentRating.objects.filter(comment__slug=value.slug, rate=arg).count()

@register.filter
def story_rate(value):
    rates = list(Rating.objects.filter(story__slug=value).values('rate').annotate(ratecount=Count('rate')))
    like = rates[1]['ratecount']
    dislike = rates[0]['ratecount']
    return like, dislike