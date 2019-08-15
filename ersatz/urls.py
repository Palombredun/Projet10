from django.urls import path

from . import views

urlpatterns = [path("Recherche/", views.search, name="search")]
