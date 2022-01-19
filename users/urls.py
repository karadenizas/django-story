from django.urls import path

from .views import (
    RegistrationCreateView,
    RegistrationDoneView,
)

app_name = 'users'

urlpatterns = [
    path('register/', RegistrationCreateView.as_view(), name='register'),
    path('register/done/', RegistrationDoneView.as_view(), name='register-done'),
]