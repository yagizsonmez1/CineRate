from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User

class AccountsTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username="alice", password="pass123", email="a@example.com"
        )

    def setUp(self):
        self.client = Client()

    def test_profile_requires_login(self):
        res = self.client.get(reverse("profile"))
        self.assertEqual(res.status_code, 302)  # Redirect to login
