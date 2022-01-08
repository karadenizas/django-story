from django.contrib import admin

from .models import Story, Character, Rating, StoryComment, CommentRating


admin.site.register(Story)
admin.site.register(Character)
admin.site.register(Rating)
admin.site.register(StoryComment)
admin.site.register(CommentRating)