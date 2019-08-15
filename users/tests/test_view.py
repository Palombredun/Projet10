from django.test import TestCase, Client
from django.contrib.auth.models import User


class LoginPageTest(TestCase):
    def setUp(self):
        User.objects.create_user(
            username="test_user",
            email="test_email@mail.com",
            password="test_userpassword123",
        )

    def test_uses_login_page(self):
        response = self.client.get("/utilisateur/connexion/")
        self.assertTemplateUsed(response, "users/login.html")

    def test_login_correctly(self):
        c = Client()
        login_infos = {"username": "test_user", "password": "test_userpassword123"}
        response = c.post("/utilisateur/connexion/", login_infos)
        self.assertEqual(response.status_code, 302)

    def test_wrong_login_infos(self):
        c = Client()
        login_infos = {"username": "test_user", "password": "wrong_password"}
        response = c.post("/utilisateur/connexion/", login_infos)
        self.assertEqual(response.status_code, 200)


class LogoutPageTest(TestCase):
    def setUp(self):
        User.objects.create_user(
            username="test_user",
            email="test_email@mail.com",
            password="test_userpassword123",
        )
        self.login_infos = {"username": "test_user", "password": "test_userpassword123"}

    def test_log_out_user(self):
        c = Client()
        response = c.post("/utilisateur/connexion/", self.login_infos)
        response = c.get("/utilisateur/deconnexion/")
        self.assertEqual(response.status_code, 302)
