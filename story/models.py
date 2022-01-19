import itertools

from django.db import models
from django.utils.text import slugify
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
from django.urls import reverse

from users.models import MyUser


class Story(models.Model):
    author = models.ForeignKey(
        MyUser,
        on_delete=models.CASCADE,
        related_name='story'
    )
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    content = models.TextField(max_length=2500, default='')
    draft = models.BooleanField(default=True)
    completed = models.BooleanField(default=False)
    expiration = models.DateTimeField(
        default=timezone.now()+timezone.timedelta(days=1),
        validators=[
            MinValueValidator(timezone.now()),
            MaxValueValidator(timezone.now()+timezone.timedelta(days=1))
        ]
    )
    added_celery = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [models.Index(fields=['draft', 'completed']),]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.title)
            
            for slug_id in itertools.count(1):
                if not Story.objects.filter(slug=self.slug).exists():
                    break
                self.slug = f'{self.slug}-{slug_id}'

        return super(Story, self).save(*args, **kwargs)

    def get_absoulte_url(self):
        return reverse('story:detail-story', kwargs={'slug': self.slug})


class StoryComment(models.Model):
    story = models.ForeignKey(
        Story,
        on_delete=models.CASCADE,
        related_name='comment'
    )
    author = models.ForeignKey(
        MyUser,
        on_delete=models.CASCADE,
        related_name='comment'
    )
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    content = models.TextField(max_length=2500, default='')
    draft = models.BooleanField(default=True)
    attachment = models.BooleanField(default=False)
    expiration = models.DateTimeField(default=timezone.now()+timezone.timedelta(days=1))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.title)
            
            for slug_id in itertools.count(1):
                if not StoryComment.objects.filter(slug=self.slug).exists():
                    break
                self.slug = f'{self.slug}-{slug_id}'

        return super(StoryComment, self).save(*args, **kwargs)


class Character(models.Model):
    story = models.ForeignKey(
        Story,
        on_delete=models.CASCADE,
        related_name='character',
        null=True,
        blank=True
    )
    comment = models.ForeignKey(
        StoryComment,
        on_delete=models.CASCADE,
        related_name='character',
        null=True,
        blank=True
    )
    name = models.CharField(max_length=100)
    age = models.PositiveIntegerField(null=True)
    species = models.CharField(max_length=100, null=True)
    gender = models.CharField(max_length=100, null=True)
    review = models.TextField(max_length=1000)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Rating(models.Model):
    story = models.ForeignKey(
        Story,
        on_delete=models.CASCADE,
        related_name='rating'
    )
    user = models.ForeignKey(
        MyUser,
        on_delete=models.CASCADE,
        related_name='rating'
    )
    rate = models.SmallIntegerField(validators=[MinValueValidator(-1), MaxValueValidator(1)], default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['story', 'user'], name='rating validation'
            )
        ]

    def __str__(self):
        return f'{self.story}'


class CommentRating(models.Model):
    comment = models.ForeignKey(
        StoryComment,
        on_delete=models.CASCADE,
        related_name='rating'
    )
    user = models.ForeignKey(
        MyUser,
        on_delete=models.CASCADE,
        related_name='comment_rating'
    )
    rate = models.SmallIntegerField(validators=[MinValueValidator(-1), MaxValueValidator(1)], default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['comment', 'user'], name='comment rating validation'
            )
        ]

    def __str__(self):
        return f'{self.created_at}'