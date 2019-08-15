from django.contrib.auth.models import User
from django.test import TestCase, Client


class ProfilePageTest(TestCase):
    def setUp(self):
        User.objects.create_user(
            username="test_user",
            email="test_email@mail.com",
            password="test_userpassword123",
        )

    def test_uses_profile_page_when_logged_in(self):
        c = Client()
        login_infos = {"username": "test_user", "password": "test_userpassword123"}
        response = c.post("/utilisateur/connexion/", login_infos)
        response = c.get("/utilisateur/mon-compte/")

        self.assertTemplateUsed(response, "profiles/profile.html")
