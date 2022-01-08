from django.http.response import Http404, HttpResponse, HttpResponseNotFound
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import ListView, CreateView, UpdateView, TemplateView
from django.utils import timezone
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count
from django.urls import reverse
from django.views.generic.detail import DetailView

from .models import Character, Story, Rating, StoryComment, CommentRating
from .forms import StoryCreateForm, StoryUpdateForm, CharacterCreateForm, StoryCommentCreateForm


class IndexListView(ListView):
    model = Story
    context_object_name = 'stories'
    template_name = 'story/index.html'
    paginate_by = 1
    queryset = Story.objects.select_related('author').filter(completed=False, draft=False)


class NewStoriesListView(ListView):
    model = Story
    context_object_name = 'stories'
    template_name = 'story/new_stories.html'
    paginate_by = 1
    queryset = Story.objects.select_related('author').filter(completed=False, draft=False)


class PopularStoriesListView(ListView):
    model = Story
    context_object_name = 'stories'
    template_name = 'story/popular_stories.html'
    paginate_by = 10
    queryset = Story.objects.filter(completed=False, draft=False) \
                .filter(rating__rate='LIKE') \
                .annotate(rate_count=Count('rating')) \
                .order_by('-rate_count')


class CompletedStoriesListView(ListView):
    model = Story
    context_object_name = 'stories'
    template_name = 'story/completed_stories.html'
    paginate_by = 10
    queryset = Story.objects.filter(completed=True, draft=False)


class StoryCreateView(CreateView):
    model = Story
    template_name = 'story/story_create.html'
    form_class = StoryCreateForm

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('story:edit-story', args=[self.object.slug])


def story_edit(request, slug):
    story = get_object_or_404(Story, slug=slug)
    story_form = StoryUpdateForm(request.POST or None, instance=story)
    character_form = CharacterCreateForm()
    characters = story.character.all()

    if request.method == "POST":
        if story_form.is_valid():
            form = story_form.save(commit=False)
            form.author = request.user
            form.save()
            return redirect('story:index')
    
    context = {
        'story': story,
        'story_form': story_form,
        'characters': characters,
        'character_form': character_form,
    }
    return render(request, 'story/story_edit.html', context)


def character_create(request, slug):
    character_form = CharacterCreateForm(request.POST or None)
    story = get_object_or_404(Story, slug=slug)
    characters = story.character.all()

    if request.method == "POST":
        if character_form.is_valid:
            form = character_form.save(commit=False)
            form.story = story
            form.save()
            return redirect('story:create-character', slug=slug)    

    context = {
        'character_form': character_form,
        'characters': characters,
    }
    return render(request, 'story/character_create.html', context)


def story_detail(request, slug):
    story = get_object_or_404(Story, slug=slug)
    characters = story.character.all()
    comments = story.comment.all()

    context = {
        'story': story,
        'characters': characters,
        'comments': comments,
    }
    return render(request, 'story/story_detail.html', context)


def story_rate(request, slug):
    story = get_object_or_404(Story, slug=slug)

    if request.method == "POST":
        rating = request.POST.get('rate')
        Rating.objects.update_or_create(story=story, user=request.user, defaults={'rate': rating})
        if rating == "LIKE":
            return HttpResponse(
                """
                    <button type="button" id="likeButton" class="btn btn-default btn-sm text-success" hx-post="{% url 'story:rate' story.slug %}" hx-target="#likeButton" hx-swap="outerHTML">
                        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-arrow-up" viewBox="0 0 16 16">
                            <path fill-rule="evenodd" d="M8 15a.5.5 0 0 0 .5-.5V2.707l3.146 3.147a.5.5 0 0 0 .708-.708l-4-4a.5.5 0 0 0-.708 0l-4 4a.5.5 0 1 0 .708.708L7.5 2.707V14.5a.5.5 0 0 0 .5.5z"/>
                        </svg>
                    </button>
                """
            )
        elif rating == "DISLIKE":
            return HttpResponse(
                """
                    <button type="button" id="dislikeButton" class="btn btn-default btn-sm text-danger" hx-post="{% url 'story:rate' story.slug %}" hx-target="#dislikeButton" hx-swap="outerHTML">
                          <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-arrow-down" viewBox="0 0 16 16">
                              <path fill-rule="evenodd" d="M8 1a.5.5 0 0 1 .5.5v11.793l3.146-3.147a.5.5 0 0 1 .708.708l-4 4a.5.5 0 0 1-.708 0l-4-4a.5.5 0 0 1 .708-.708L7.5 13.293V1.5A.5.5 0 0 1 8 1z"/>
                          </svg>
                    </button>      
                """
            )


def comment_rate(request, slug):
    comment = get_object_or_404(StoryComment, slug=slug)

    if request.method == "POST":
        rating = request.POST.get('rate')
        CommentRating.objects.update_or_create(comment=comment, user=request.user, defaults={'rate': rating})
        if rating == "LIKE":
            return HttpResponse(
                """
                    <button type="button" id="c{{forloop.counter}}commentlikeButton" class="btn btn-default btn-sm text-success" hx-post="{% url 'story:rate' story.slug %}" hx-target="#c{{forloop.counter}}commentlikeButton" hx-swap="outerHTML">
                        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-arrow-up" viewBox="0 0 16 16">
                            <path fill-rule="evenodd" d="M8 15a.5.5 0 0 0 .5-.5V2.707l3.146 3.147a.5.5 0 0 0 .708-.708l-4-4a.5.5 0 0 0-.708 0l-4 4a.5.5 0 1 0 .708.708L7.5 2.707V14.5a.5.5 0 0 0 .5.5z"/>
                        </svg>
                    </button>
                """
            )
        elif rating == "DISLIKE":
            return HttpResponse(
                """
                    <button type="button" id="c{{forloop.counter}}commentdislikeButton" class="btn btn-default btn-sm text-danger" hx-post="{% url 'story:rate' story.slug %}" hx-target="#c{{forloop.counter}}commentdislikeButton" hx-swap="outerHTML">
                          <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-arrow-down" viewBox="0 0 16 16">
                              <path fill-rule="evenodd" d="M8 1a.5.5 0 0 1 .5.5v11.793l3.146-3.147a.5.5 0 0 1 .708.708l-4 4a.5.5 0 0 1-.708 0l-4-4a.5.5 0 0 1 .708-.708L7.5 13.293V1.5A.5.5 0 0 1 8 1z"/>
                          </svg>
                    </button>      
                """
            )

def comment_create(request, slug):
    if request.method == "POST" and  request.POST.get('deger'):
        story = Story.objects.get(slug=slug)
        qs = StoryComment.objects.create(story=story, author=request.user, title=request.POST.get('deger'))
        return redirect('story:comment-edit', slug=qs.slug)
    else:
        return HttpResponseNotFound('<h1>Page not found</h1>')


def comment_character_create(request, slug):
    character_form = CharacterCreateForm(request.POST or None)
    comment = get_object_or_404(StoryComment, slug=slug)
    characters = comment.character.all()

    if request.method == "POST":
        if character_form.is_valid:
            form = character_form.save(commit=False)
            form.comment = comment
            form.save()
            return redirect('story:create-comment-character', slug=slug)    

    context = {
        'character_form': character_form,
        'characters': characters,
    }
    return render(request, 'story/character_create.html', context)


def comment_edit(request, slug):
    comment = StoryComment.objects.get(slug=slug)
    comment_form = StoryCommentCreateForm(request.POST or None, instance=comment)
    character_form = CharacterCreateForm()
    story_characters = Character.objects.filter(story=comment.story)
    comment_characters = Character.objects.filter(comment=comment)

    if request.method == "POST":
        if comment_form.is_valid():
            form = comment_form.save(commit=False)
            form.author = request.user
            form.save()
            return redirect('story:detail-story', slug=comment.story.slug)

    context = {
        'comment': comment,
        'comment_form': comment_form,
        'character_form': character_form,
        'story_characters': story_characters,
        'characters': comment_characters,
    }
    return render(request, 'story/comment_edit.html', context)


class StoryCommentDetailView(DetailView):
    model = StoryComment
    template_name = 'story/comment_detail.html'
    context_object_name = 'comment'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['characters'] = Character.objects.filter(comment__slug=self.kwargs.get('slug'))
        return context


class TestView(ListView):
    model = Story
    template_name = 'test.html'
    context_object_name = 'stories'
    paginate_by = 10
    queryset = Story.objects.select_related('author').filter(completed=False, draft=False)
