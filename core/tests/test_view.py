from django.test import TestCase


class HomePageTest(TestCase):
    def test_uses_home_template(self):
        response = self.client.get("/")
        self.assertTemplateUsed(response, "core/home.html")


class LegaleNoticePageTest(TestCase):
    def test_uses_legale_notice_template(self):
        response = self.client.get("/Mentions-Legales/")
        self.assertTemplateUsed(response, "core/legale_notice.html")
