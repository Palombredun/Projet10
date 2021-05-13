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
        products = Product.objects.filter(
            product_name__icontains=query)

        if products.count() == 0:
            return render(request, "ersatz/result.html")
        else:
            potential_replacements = []
            for product in products:
                # find the best match for the query (highest ratio)
                potential_replacements.append(
                    (
                        product,
                        SequenceMatcher(None, query, product.product_name).ratio(),
                    )
                )
            potential_replacements.sort(key=lambda x: x[1])
            product_to_replace = potential_replacements[-1][0]


            replacements = Product.objects.filter(
                bottom_category=product_to_replace.bottom_category
            ).order_by("nutriscore")
            if len(replacements) < 3:
                replacements = Product.objects.filter(
                    middle_category=product_to_replace.middle_category
                ).order_by("nutriscore")
            else:
                replacements = Product.objects.filter(
                    top_category=product_to_replace.top_category
                ).order_by("nutriscore")

            ersatz = []
            for product in replacements:
                if product.nutriscore < product_to_replace.nutriscore:
                    ersatz.append(product)

            # return only the top 6 of the products
            return render(
                request,
                "ersatz/result.html",
                {"search": product_to_replace, "products": ersatz[:6]},
            )
    else:
        return redirect("home")
