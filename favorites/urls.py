from django.urls import path
from favorites.views import FavoriteView

urlpatterns = [path("favoris/", FavoriteView.as_view(), name="favorites")]
