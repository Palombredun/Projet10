from django.test import TestCase


class SignupPageTest(TestCase):
    def test_uses_signup_page(self):
        response = self.client.get("/utilisateur/inscription/")
        self.assertTemplateUsed(response, "signup/signup.html")
