from django.urls import path

from . import views

urlpatterns = [path("mon-compte/", views.profile, name="profile")]
