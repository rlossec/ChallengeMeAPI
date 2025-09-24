# python manage.py test accounts.tests.test_user_list
from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework.test import APITestCase
from rest_framework import status

User = get_user_model()


class TestUserListEndpoint(APITestCase):
    def setUp(self):
        self.simple_user = User.objects.create_user(
            username="simpleuser",
            email="simpleuser@example.com",
            password="password12"
        )
        self.simple_user1 = User.objects.create_user(
            username="simple_user1",
            email="user1@example.com",
            password="password123"
        )
        self.simple_user2 = User.objects.create_user(
            username="simple_user2",
            email="user2@example.com",
            password="password223"
        )
        self.staff_user1 = User.objects.create_user(
            username="staffuser1",
            email="staffuser1@example.com",
            password="password145",
            is_staff=True
        )
        self.staff_user2 = User.objects.create_user(
            username="staffuser2",
            email="staffuser2@example.com",
            password="password245",
            is_staff=True
        )
        self.superuser1 = User.objects.create_superuser(
            username="superuser1",
            email="superuser1@example.com",
            password="password189"
        )
        self.superuser2 = User.objects.create_superuser(
            username="superuser2",
            email="superuser2@example.com",
            password="password289"
        )
        self.user_list_url = reverse('user-list')

    # Success
    def test_simple_user_can_only_see_themselves(self):
        """Test pour vérifier qu'un utilisateur normal ne voit que lui-même"""
        self.client.login(username="simpleuser", password="password12")
        response = self.client.get(self.user_list_url)
        emails = [user['email'] for user in response.data]

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['email'], self.simple_user.email)

        self.assertNotIn(self.simple_user1.email, emails)
        self.assertNotIn(self.staff_user1.email, emails)

    def test_staff_user_can_see_all_users(self):
        """Test pour vérifier qu'un administrateur peut voir tous les utilisateurs"""
        nb_users = User.objects.count()
        self.client.login(username="superuser1", password="password189")
        response = self.client.get(self.user_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)
        self.assertEqual(len(response.data), nb_users)

        # Vérifie que tous les utilisateurs sont présents dans la réponse
        emails = [user['email'] for user in response.data]
        self.assertIn(self.simple_user1.email, emails)
        self.assertIn(self.staff_user1.email, emails)
        self.assertIn(self.superuser1.email, emails)
        # Hidden fields
        user_data = response.data[0]
        self.assertNotIn('is_staff', user_data)
        self.assertNotIn('is_superuser', user_data)

    def test_superadmin_user_can_see_all_users(self):
        """Test pour vérifier qu'un administrateur peut voir tous les utilisateurs"""
        nb_users = User.objects.count()
        self.client.login(username="staffuser1", password="password145")
        response = self.client.get(self.user_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)
        self.assertEqual(len(response.data), nb_users)

        # Vérifie que tous les utilisateurs sont présents dans la réponse
        emails = [user['email'] for user in response.data]
        self.assertIn(self.simple_user1.email, emails)
        self.assertIn(self.staff_user1.email, emails)
        self.assertIn(self.superuser1.email, emails)

    # 401
    ## Unauthenticated
    def test_access_user_list_unauthenticated(self):
        response = self.client.get(self.user_list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
