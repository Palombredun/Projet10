from django.urls import path

from . import views

urlpatterns = [path("produit/<int:id>/", views.product, name="product")]
