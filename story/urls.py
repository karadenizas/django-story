from django.urls import path

from .views import (
    IndexListView,
    NewStoriesListView,
    PopularStoriesListView,
    CompletedStoriesListView,

    StoryCreateView,
    StoryUpdateView,
    StoryCommentListView,
    ## character
    HtmxCharacterCreateView,
    HtmxCommentCharacterCreateView,
    ## rate
    # story_rate,
    # comment_rate,
    HtmxRateUpdateView,
    ## comment
    comment_create,
    StoryCommentDetailView,
    StoryCommentUpdateView,
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
    path('edit/<str:slug>/', StoryUpdateView.as_view(), name='edit-story'),
    path('detail/<str:slug>/', StoryCommentListView.as_view(), name='detail-story'),
    ## Characters
    path('create-character/<str:slug>/', HtmxCharacterCreateView.as_view(), name='create-character'),
    path('create-comment-character/<str:slug>/', HtmxCommentCharacterCreateView.as_view(), name='create-comment-character'),
    ## Rate
    path('check-rate/<str:slug>/', HtmxRateUpdateView.as_view(), name='rate'),
    ## Comment
    path('create/comment/<str:slug>/',comment_create, name='comment-create' ),
    path('create/edit/<str:slug>/',StoryCommentUpdateView.as_view(), name='comment-edit' ),
    path('comment/detail/<str:slug>/', StoryCommentDetailView.as_view(), name='comment-detail'),
    ## TEST
    path('test/', TestView.as_view())
]