from django.urls import path

from .views import (
    IndexListView,
    NewStoriesListView,
    PopularStoriesListView,
    CompletedStoriesListView,

    StoryCreateView,
    character_create,
    story_edit,
    story_detail,
    ## rate
    story_rate,
    comment_rate,
    ## comment
    comment_create,
    comment_edit,
    comment_character_create,
    StoryCommentDetailView,
    #### TEST
    TestView,
)

app_name = 'story'

urlpatterns = [
    path('', IndexListView.as_view(), name='index'),
    path('new-stories/', NewStoriesListView.as_view(), name='new-stories'),
    path('popular-stories/', PopularStoriesListView.as_view(), name='popular-stories'),
    path('completed-stories/', CompletedStoriesListView.as_view(), name='completed-stories'),
    ## Stories
    path('create/', StoryCreateView.as_view(), name='create-story'),
    path('edit/<str:slug>/', story_edit, name='edit-story'),
    path('detail/<str:slug>/', story_detail, name='detail-story'),
    ## Characters
    path('create-character/<str:slug>/', character_create, name='create-character'),
    path('create-comment-character/<str:slug>/', comment_character_create, name='create-comment-character'),
    ## Rate
    path('check-story-rate/<str:slug>/', story_rate, name='story-rate'),
    path('check-comment-rate/<str:slug>/', comment_rate, name='comment-rate'),
    ## Comment
    path('create/comment/<str:slug>/',comment_create, name='comment-create' ),
    path('create/edit/<str:slug>/',comment_edit, name='comment-edit' ),
    path('comment/detail/<str:slug>/', StoryCommentDetailView.as_view(), name='comment-detail'),
    ## TEST
    path('test/', TestView.as_view())
]