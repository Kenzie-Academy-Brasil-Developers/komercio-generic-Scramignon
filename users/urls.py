from django.urls import path
from . import views

from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path("login/", obtain_auth_token),
    path("accounts/", views.UserView.as_view()),
    path("accounts/newest/<int:num>", views.listNewUsersView.as_view())
]