from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("Mentions-Legales/", views.legale_notice, name="legale_notice"),
]
