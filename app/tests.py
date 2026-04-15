from django.contrib.auth.models import Group, User
from django.test import TestCase
from django.urls import reverse

from app.models import Client, Menu, Order


class RegistrationTest(TestCase):
    def test_user_registration(self):
        response = self.client.post(
            reverse("register"),
            {
                "username": "testuser",
                "nom": "Test",
                "prenom": "User",
                "password1": "VeryStrongPass123!",
                "password2": "VeryStrongPass123!",
                "birthday": "2000-01-01",
                "gender": "M",
                "phone": "123",
                "address": "123",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username="testuser").exists())


class AuthTest(TestCase):
    def test_login(self):
        User.objects.create_user("loginuser", "login@test.com", "pass12345Ab!")
        response = self.client.post(
            reverse("connect"),
            {"username": "loginuser", "password": "pass12345Ab!"},
        )
        self.assertEqual(response.status_code, 302)


class OrderTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user("test", "test@test.com", "pass12345Ab!")
        self.client.login(username="test", password="pass12345Ab!")
        self.profile = Client.objects.create(user=self.user)
        self.menu = Menu.objects.create(name="Burger", price=10, description="Yummy")

    def test_create_order(self):
        response = self.client.get(reverse("new_order", args=[self.menu.id]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Order.objects.count(), 1)

    def test_role_permissions_for_chef_view(self):
        chef_group, _ = Group.objects.get_or_create(name="Chef")
        self.user.groups.add(chef_group)
        Order.objects.create(client=self.profile, menu=self.menu, delivered=False)
        response = self.client.get(reverse("order"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Burger")
