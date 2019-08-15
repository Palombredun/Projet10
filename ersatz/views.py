from difflib import SequenceMatcher

from django.shortcuts import render, redirect

from products.models import Product, Category


def search(request):
    """
    If the user's query has not match in the database, simply return the templates.
    Else, select the product corresponding the most to the query and
    return the template and up to 6 products with a better nutriscore than the query.
    """
    if "query" in request.GET:
        query = request.GET["query"]
        products = Product.objects.filter(product_name__icontains=query)

        if products.count() == 0:
            return render(request, "ersatz/result.html")
        else:
            foo = []
            for product in products:
                # find the best match for the query (highest ratio)
                foo.append(
                    (
                        product,
                        SequenceMatcher(None, query, product.product_name).ratio(),
                    )
                )
            foo.sort(key=lambda x: x[1])

            product_to_replace = foo[-1][0]

            simili_products = Product.objects.filter(
                category=product_to_replace.category
            ).order_by("nutriscore")

            ersatz = []
            for prod in simili_products:
                if prod.nutriscore < product_to_replace.nutriscore:
                    ersatz.append(prod)

            # return only the top 6 of the products
            return render(
                request,
                "ersatz/result.html",
                {"search": product_to_replace, "products": ersatz[:6]},
            )
    else:
        return redirect("home")
