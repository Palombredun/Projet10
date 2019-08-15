from django.test import TestCase

from products.models import Category, Product


class ErsatzPageTest(TestCase):
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
        Product.objects.create(
            product_name="ersatz1",
            nutriscore="b",
            image_url="https://test_image.com",
            product_url="https://testopenfoodfacts.org",
            category=c,
        )
        Product.objects.create(
            product_name="ersatz2",
            nutriscore="a",
            image_url="https://test_image.com",
            product_url="https://testopenfoodfacts.org",
            category=c,
        )

    def test_uses_result_template(self):
        response = self.client.get("/Recherche/?query=coca")
        self.assertTemplateUsed(response, "ersatz/result.html")

    def test_get_request_result(self):
        response = self.client.get("/Recherche/?query=test1")
        content = response.content.decode("utf8")
        self.assertInHTML('<p class="query-name">test1</p>', content)

    def test_get_zero_result(self):
        response = self.client.get("/Recherche/?query=azyfre")
        content = response.content.decode("utf8")
        self.assertInHTML(
            """<div class="row"><p>Aucun produit n'a été trouvé.</p></div>""", content
        )
