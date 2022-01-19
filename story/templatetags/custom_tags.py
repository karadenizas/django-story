from django import template
from django.db.models import Count, Sum
from django.db.models.functions import Coalesce

from ..models import Rating, CommentRating, Story

register = template.Library()

@register.filter
def comment_rate(value):
    rate = CommentRating.objects.filter(comment__slug=value).aggregate(total_rate=Coalesce(Sum('rate'), 0))
    return rate['total_rate']

@register.filter
def story_rate(value):
    rate = Rating.objects.filter(story__slug=value).aggregate(total_rate=Coalesce(Sum('rate'), 0))
    return rate['total_rate']
