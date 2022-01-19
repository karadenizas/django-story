from django.http.response import Http404, HttpResponse, HttpResponseNotFound
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import ListView, CreateView, UpdateView
from django.utils import timezone
from django.db.models import Count
from django.urls import reverse
from django.views.generic.detail import DetailView
from django.db.models import Count, Sum
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

from .models import Character, Story, Rating, StoryComment, CommentRating
from .forms import StoryCreateForm, StoryUpdateForm, CharacterCreateForm, StoryCommentCreateForm
from .tasks import expiration_task

# User Permission
class IsOwnerOnlyMixin(object):

    def has_permissions(self):
        return self.get_object().author == self.request.user

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permissions():
            raise Http404('You do not have permission.')
        return super(IsOwnerOnlyMixin, self).dispatch(request, *args, **kwargs)


class IndexListView(ListView):
    model = Story
    context_object_name = 'stories'
    template_name = 'story/index.html'
    paginate_by = 10
    queryset = Story.objects.select_related('author').filter(completed=False, draft=False)


class NewStoriesListView(ListView):
    model = Story
    context_object_name = 'stories'
    template_name = 'story/new_stories.html'
    paginate_by = 10
    queryset = Story.objects.select_related('author').filter(completed=False, draft=False)


class PopularStoriesListView(ListView):
    model = Story
    context_object_name = 'stories'
    template_name = 'story/popular_stories.html'
    paginate_by = 10
    queryset = Story.objects.select_related('author').filter(completed=False, draft=False).filter(rating__rate__isnull=False).annotate(total_rate=Sum('rating__rate')).order_by('-total_rate')
 

class CompletedStoriesListView(ListView):
    model = Story
    context_object_name = 'stories'
    template_name = 'story/completed_stories.html'
    paginate_by = 10
    queryset = Story.objects.select_related('author').filter(completed=True, draft=False)


class StoryCreateView(LoginRequiredMixin, CreateView):
    model = Story
    template_name = 'story/story_create.html'
    form_class = StoryCreateForm
    login_url = 'login'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('story:edit-story', args=[self.object.slug])


class StoryUpdateView(LoginRequiredMixin, IsOwnerOnlyMixin, UpdateView):
    model = Story
    template_name = 'story/story_edit.html'
    form_class = StoryUpdateForm
    character_form_class = CharacterCreateForm
    login_url = 'login'

    def get_initial(self):
        initial = super(StoryUpdateView, self).get_initial()
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['story'] = get_object_or_404(Story, slug=self.object.slug)
        context['characters'] = self.object.character.all()
        context['story_form'] = self.get_form()
        context['character_form'] = self.character_form_class()
        context['loop_times'] = range(1,25) # for expiration time detect
        return context

    def form_valid(self, form):
        form.instance.author = self.request.user
        if self.object.added_celery == False:
            hour = int(self.request.POST.get('hour')) # expiration time
            expiration_time = timezone.now() + timezone.timedelta(hours=hour)
            form.instance.expiration = expiration_time
            self.object.added_celery = True
            expiration_task.apply_async([self.object.id], eta=expiration_time, kwargs={'story-id': self.object.id})
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('story:detail-story', args=[self.object.slug])


# Htmx create character view for StoryUpdateView
class HtmxCharacterCreateView(LoginRequiredMixin, CreateView):
    model = Character
    template_name = 'story/character_create.html'
    form_class = CharacterCreateForm
    login_url = 'login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['characters'] = Character.objects.filter(story__slug=self.kwargs['slug'])
        return context

    def form_valid(self, form):
        form.instance.story = Story.objects.get(slug=self.kwargs['slug'])
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('story:create-character', args=[self.kwargs['slug']])


class StoryCommentListView(ListView):
    model = StoryComment
    template_name = 'story/story_detail.html'
    context_object_name = 'comments'
    paginate_by = 10

    def get_queryset(self):
        queryset = StoryComment.objects.select_related('story', 'author').filter(story__slug=self.kwargs['slug'])
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['story'] = Story.objects.select_related('author').get(slug=self.kwargs['slug'])
        context['characters'] = Character.objects.select_related('story').filter(story__slug=self.kwargs['slug'])
        context['attachment_stories'] = StoryComment.objects.filter(story__slug=self.kwargs['slug'], attachment=True)
        return context


# create comment with title and continue to StoryCommentUpdateView
@login_required(login_url='login')
def comment_create(request, slug):
    if request.method == "POST":
        story = Story.objects.get(slug=slug)
        qs = StoryComment.objects.create(story=story, author=request.user, title=request.POST.get('title'))
        return redirect('story:comment-edit', slug=qs.slug)
    else:
        return HttpResponseNotFound('<h1>Page not found</h1>')


class StoryCommentUpdateView(LoginRequiredMixin, IsOwnerOnlyMixin, UpdateView):
    model = StoryComment
    template_name = 'story/comment_edit.html'
    form_class = StoryCommentCreateForm
    character_form_class = CharacterCreateForm
    login_url = 'login'

    def get_initial(self):
        initial = super(StoryCommentUpdateView, self).get_initial()
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment'] = get_object_or_404(StoryComment, slug=self.object.slug)
        context['characters'] = self.object.character.all()
        context['story_characters'] = self.object.story.character.all()
        context['comment_form'] = self.get_form()
        context['character_form'] = self.character_form_class()
        return context

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('story:comment-detail', args=[self.object.slug])


class HtmxCommentCharacterCreateView(LoginRequiredMixin, CreateView):
    model = Character
    template_name = 'story/character_create.html'
    form_class = CharacterCreateForm
    login_url = 'login'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['characters'] = Character.objects.filter(comment__slug=self.kwargs['slug'])
        return context
    
    def form_valid(self, form):
        form.instance.comment = StoryComment.objects.get(slug=self.kwargs['slug'])
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse('story:create-comment-character', args=[self.kwargs['slug']])


class HtmxRateUpdateView(LoginRequiredMixin ,UpdateView):

    def post(self, request, *args, **kwargs):
        # Story Rate
        if request.POST.get('story_rate'):
            story = get_object_or_404(Story, slug=self.kwargs['slug'])
            Rating.objects.update_or_create(story=story, user=self.request.user, defaults={'rate': request.POST.get('story_rate')})
            if request.POST.get('story_rate') == '1':
                return HttpResponse(
                    """
                        <button type="button" id="likeButton" class="btn btn-default btn-sm text-success" hx-post="{% url 'story:rate' story.slug %}" hx-target="#likeButton" hx-swap="outerHTML">
                            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-chevron-up" viewBox="0 0 16 16">
                            <path fill-rule="evenodd" d="M7.646 4.646a.5.5 0 0 1 .708 0l6 6a.5.5 0 0 1-.708.708L8 5.707l-5.646 5.647a.5.5 0 0 1-.708-.708l6-6z"/>
                            </svg>
                        </button>
                    """
                )
        
            elif request.POST.get('story_rate') == '-1':
                return HttpResponse(
                    """
                        <button type="button" id="dislikeButton" class="btn btn-default btn-sm text-danger" hx-post="{% url 'story:rate' story.slug %}" hx-target="#dislikeButton" hx-swap="outerHTML">
                            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-chevron-down" viewBox="0 0 16 16">
                            <path fill-rule="evenodd" d="M1.646 4.646a.5.5 0 0 1 .708 0L8 10.293l5.646-5.647a.5.5 0 0 1 .708.708l-6 6a.5.5 0 0 1-.708 0l-6-6a.5.5 0 0 1 0-.708z"/>
                            </svg>
                        </button>      
                    """
                )
            else:
                return HttpResponse('Something went wrong!')

        # Comment Rate
        elif request.POST.get('comment_rate'):
            comment = get_object_or_404(StoryComment, slug=self.kwargs['slug'])
            CommentRating.objects.update_or_create(comment=comment, user=self.request.user, defaults={'rate': request.POST.get('comment_rate')})
            if request.POST.get('comment_rate') == '1':
                return HttpResponse(
                    """
                        <button type="button" id="c{{forloop.counter}}commentlikeButton" class="btn btn-default btn-sm text-success" hx-post="{% url 'story:rate' story.slug %}" hx-target="#c{{forloop.counter}}commentlikeButton" hx-swap="outerHTML">
                            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-chevron-up" viewBox="0 0 16 16">
                            <path fill-rule="evenodd" d="M7.646 4.646a.5.5 0 0 1 .708 0l6 6a.5.5 0 0 1-.708.708L8 5.707l-5.646 5.647a.5.5 0 0 1-.708-.708l6-6z"/>
                            </svg>
                        </button>
                    """
                )
            elif request.POST.get('comment_rate') == '-1':
                return HttpResponse(
                    """
                        <button type="button" id="c{{forloop.counter}}commentdislikeButton" class="btn btn-default btn-sm text-danger" hx-post="{% url 'story:rate' story.slug %}" hx-target="#c{{forloop.counter}}commentdislikeButton" hx-swap="outerHTML">
                            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-chevron-down" viewBox="0 0 16 16">
                            <path fill-rule="evenodd" d="M1.646 4.646a.5.5 0 0 1 .708 0L8 10.293l5.646-5.647a.5.5 0 0 1 .708.708l-6 6a.5.5 0 0 1-.708 0l-6-6a.5.5 0 0 1 0-.708z"/>
                            </svg>
                        </button>      
                    """
                )
        else:
            return super().post(request, *args, **kwargs)


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