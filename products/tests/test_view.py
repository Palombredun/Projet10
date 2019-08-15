from django.test import TestCase

from products.models import Category, Product


class ProductPageTest(TestCase):
    def setUp(self):
        c = Category.objects.create(category_name="test_category")
        c.save()

        Product.objects.create(
            product_name="test1",
            nutriscore="e",
            image_url="https://test_image.com",
            product_url="https://testopenfoodfacts.org",
            category=c,
        )
        self.product = Product.objects.get(product_name="test1")

    def test_uses_product_page(self):
        response = self.client.get("/produit/" + str(self.product.id) + "/")
        self.assertTemplateUsed(response, "products/product.html")

    def test_get_product_page(self):
        response = self.client.get("/produit/" + str(self.product.id) + "/")
        content = response.content.decode("utf8")
        self.assertInHTML("""<p>test1</p>""", content)
        self.assertInHTML(
            """<img src="/static/products/img/nutriscore_E.png" class="nutriscore" alt="nutriscore-E">""",
            content,
        )
