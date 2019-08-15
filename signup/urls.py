from django.urls import path

from . import views

urlpatterns = [path("inscription/", views.signup, name="signup")]
