from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views import View

from products.models import Product


class FavoriteView(View):
    template_name = "favorites/favorites.html"

    @method_decorator(login_required)
    def get(self, request):
        current_user = request.user
        foo = Product.favorite.through.objects.filter(user__id=current_user.id)
        favorites = []
        for bar in foo:
            favorites.append(Product.objects.get(id=bar.product_id))
        return render(request, self.template_name, {"favorites": favorites})

    @method_decorator(login_required)
    def post(self, request):
        current_user = request.user
        id_product = request.POST["id_product"]
        product = Product.objects.get(id=id_product)
        if (
            Product.favorite.through.objects.filter(user__id=current_user.id)
            .filter(product_id=id_product)
            .count()
            == 0
        ):
            product.favorite.add(current_user)
        return redirect("favorites")
