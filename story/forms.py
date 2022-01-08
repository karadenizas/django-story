from django import forms

from .models import Story, Character, StoryComment


class StoryCreateForm(forms.ModelForm):

    class Meta:
        model = Story
        fields = ['title']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control form-control-sm', 'placeholder': 'enter a story name'}),
        }


class StoryUpdateForm(forms.ModelForm):

    class Meta:
        model = Story
        fields = ['title', 'content', 'draft']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control form-control-sm', 'placeholder': 'enter a story name'}),
            'content': forms.Textarea(attrs={'class': 'form-control form-control-sm', 'placeholder': 'story'}),
            'draft': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {'title': 'Story Name', 'draft': 'Draft'}


class CharacterCreateForm(forms.ModelForm):

    class Meta:
        model = Character
        fields = ['name', 'age', 'species', 'gender', 'review']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control form-control-sm', 'placeholder': 'name'}),
            'age': forms.NumberInput(attrs={'class': 'form-control form-control-sm', 'placeholder': 'age'}),
            'species': forms.TextInput(attrs={'class': 'form-control form-control-sm', 'placeholder': 'species'}),
            'gender': forms.TextInput(attrs={'class': 'form-control form-control-sm', 'placeholder': 'gender'}),
            'review': forms.Textarea(attrs={'class': 'form-control form-control-sm', 'placeholder': 'review'}),
        }

class StoryCommentCreateForm(forms.ModelForm):

    class Meta:
        model = StoryComment
        fields = ['title', 'content', 'draft']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control form-control-sm', 'placeholder': 'enter a story name'}),
            'content': forms.Textarea(attrs={'class': 'form-control form-control-sm', 'placeholder': 'story'}),
            'draft': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {'title': 'Continue Story Title', 'draft': 'Draft'}