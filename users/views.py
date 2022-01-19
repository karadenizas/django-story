from django.http.response import HttpResponse
from django.shortcuts import render
from django.views.generic import CreateView, TemplateView

from .forms import UserCreationForm


class RegistrationCreateView(CreateView):
    form_class = UserCreationForm
    template_name = 'registration/register.html'
    success_url = 'done/'


class RegistrationDoneView(TemplateView):
    template_name = 'registration/register_done.html'