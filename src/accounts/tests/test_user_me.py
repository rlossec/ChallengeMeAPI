# python manage.py test accounts.tests.test_user_me
from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.test import APITestCase

from accounts.tests import AUTHENTICATION_MISSING, MANDATORY_FIELD_ERROR_MESSAGE, \
    INVALID_EMAIL_ERROR_MESSAGE, USERNAME_ALREADY_TAKEN_ERROR_MESSAGE, EMAIL_ALREADY_TAKEN_ERROR_MESSAGE

User = get_user_model()


class TestUserMeEndpoint(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='ValidPassword123!',
            first_name='John',
            last_name='Doe'
        )
        self.token = self.client.post(reverse('jwt-create'), {
            'username': 'testuser',
            'password': 'ValidPassword123!'
        }).data['access']
        self.user_me_url = reverse('user-me')

    # Retrieve
    def test_get_user_me(self):
        """Test pour récupérer les informations de l'utilisateur"""
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        response = self.client.get(self.user_me_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Available field
        self.assertIn('id', response.data)
        self.assertEqual(response.data['id'], self.user.id)
        self.assertIn('email', response.data)
        self.assertEqual(response.data['email'], self.user.email)
        self.assertIn('username', response.data)
        self.assertEqual(response.data['username'], self.user.username)
        self.assertIn('first_name', response.data)
        self.assertEqual(response.data['first_name'], self.user.first_name)
        self.assertIn('last_name', response.data)
        self.assertEqual(response.data['last_name'], self.user.last_name)
        # Missing fields
        self.assertNotIn('password', response.data)

    ## Unauthenticated
    def test_get_user_me_without_authentication(self):
        response = self.client.get(self.user_me_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('detail', response.data)
        self.assertEqual(response.data['detail'], AUTHENTICATION_MISSING)
        self.assertNotIn('username', response.data)

    # Update
    ## Success
    def test_put_user_me(self):
        """Test pour mettre à jour les informations de l'utilisateur (sans changer le nom d'utilisateur)"""
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        response = self.client.put(self.user_me_url, {
            'id': 9999,
            'username': 'newusername',

            'email': 'newemail@example.com',
            'first_name': 'Pau',
            'last_name': 'Gasol'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertNotEqual(self.user.id, 9999)
        self.assertEqual(self.user.username, 'testuser')
        self.assertEqual(response.data['username'], 'testuser')
        # Modifications
        self.assertEqual(self.user.first_name, 'Pau')
        self.assertEqual(response.data['first_name'], 'Pau')
        self.assertEqual(self.user.last_name, 'Gasol')
        self.assertEqual(response.data['last_name'], 'Gasol')
        # Email
        self.assertEqual(self.user.email, 'newemail@example.com')
        self.assertEqual(response.data['email'], 'newemail@example.com')
        self.assertFalse(self.user.is_active)

    def test_put_user_me_unmodifiable_username(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        response = self.client.put(self.user_me_url, {
            'email': 'updatedemail@example.com',
            'username': 'newusername'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, 'testuser')
        self.assertEqual(self.user.email, 'updatedemail@example.com')
        self.assertFalse(self.user.is_active)

    ## Unauthenticated
    def test_put_user_me_without_authentication(self):
        response = self.client.put(self.user_me_url, {'email': 'unauthenticated@example.com'})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('detail', response.data)
        self.assertEqual(response.data['detail'], AUTHENTICATION_MISSING)

    ## Missing fields
    def test_put_user_me_missing_fields(self):
        """Test pour vérifier que la mise à jour échoue avec des champs manquants"""
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        response = self.client.put(self.user_me_url, {
            'first_name': 'Pau',
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data)
        self.assertEqual(response.data['email'][0], MANDATORY_FIELD_ERROR_MESSAGE)
        self.assertEqual(self.user.first_name, 'John')

    ## Invalid
    def test_put_user_me_invalid_email_format(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        response = self.client.put(self.user_me_url, {'email': 'notanemail'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data)
        self.assertEqual(response.data['email'][0], INVALID_EMAIL_ERROR_MESSAGE)
        self.assertTrue(self.user.is_active)

    def test_put_user_me_email_already_taken(self):
        """Test pour vérifier que l'email ne peut pas être changé à un email déjà utilisé"""
        User.objects.create_user(
            username='anotheruser',
            email='takenemail@example.com',
            password='AnotherValidPassword123!'
        )
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        response = self.client.put(self.user_me_url, {'email': 'takenemail@example.com'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data)
        self.assertEqual(response.data['email'][0], EMAIL_ALREADY_TAKEN_ERROR_MESSAGE)
        self.assertTrue(self.user.is_active)

    # Partial update
    ## Success
    def test_patch_user_me(self):
        """Test pour mettre à jour partiellement les informations de l'utilisateur (sans changer le nom d'utilisateur)"""
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        response = self.client.patch(self.user_me_url, {
            'id': 9999,
            'username': 'newusername',

            'email': 'newemail@example.com',
            'first_name': 'Pau',
            'last_name': 'Gasol'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()

        self.assertNotEqual(self.user.id, 9999)
        self.assertEqual(self.user.username, 'testuser')
        self.assertEqual(response.data['username'], 'testuser')
        # Modifications
        self.assertEqual(self.user.first_name, 'Pau')
        self.assertEqual(response.data['first_name'], 'Pau')
        self.assertEqual(self.user.last_name, 'Gasol')
        self.assertEqual(response.data['last_name'], 'Gasol')

        self.assertEqual(self.user.email, 'newemail@example.com')
        self.assertEqual(response.data['email'], 'newemail@example.com')
        self.assertFalse(self.user.is_active)

        self.assertEqual(self.user.first_name, 'Pau')

    def test_patch_user_me_without_email(self):
        """Test pour vérifier que la mise à jour réussi sans email"""
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        response = self.client.patch(self.user_me_url, {
            'first_name': 'Pau',
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.user.first_name, 'John')

    ## Unauthenticated
    def test_patch_user_me_without_authentication(self):
        response = self.client.patch(self.user_me_url, {'email': 'unauthenticated@example.com'})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('detail', response.data)
        self.assertEqual(response.data['detail'], AUTHENTICATION_MISSING)

    ## Invalid field
    def test_patch_user_me_invalid_email_format(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        response = self.client.patch(self.user_me_url, {'email': 'notanemail'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data)
        self.assertEqual(response.data['email'][0], INVALID_EMAIL_ERROR_MESSAGE)
        self.assertTrue(self.user.is_active)

    def test_patch_user_me_email_already_taken(self):
        """Test pour vérifier que l'email ne peut pas être changé à un email déjà utilisé"""
        User.objects.create_user(
            username='anotheruser',
            email='takenemail@example.com',
            password='AnotherValidPassword123!'
        )
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        response = self.client.patch(self.user_me_url, {'email': 'takenemail@example.com'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data)
        self.assertEqual(response.data['email'][0], EMAIL_ALREADY_TAKEN_ERROR_MESSAGE)
        self.assertTrue(self.user.is_active)

    # Delete
    def test_delete_user_me(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        response = self.client.delete(self.user_me_url, {'current_password': 'ValidPassword123!'})
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        # Vérifier que l'utilisateur est supprimé
        response = self.client.get(self.user_me_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    ## Unauthenticated
    def test_delete_user_me_unauthenticated(self):
        response = self.client.delete(self.user_me_url, {'current_password': 'ValidPassword123!'})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('detail', response.data)
        self.assertEqual(response.data['detail'], AUTHENTICATION_MISSING)

    ## Missing field
    def test_delete_user_me_without_password(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        response = self.client.delete(self.user_me_url, {})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('current_password', response.data)
        self.assertEqual(response.data['current_password'][0], MANDATORY_FIELD_ERROR_MESSAGE)


class TestUserGetMe(APITestCase):
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

    def test_user_me_as_simple_user(self):
        self.client.login(username="simpleuser", password="password12")
        response = self.client.get(reverse("user-me"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], self.simple_user.username)

    def test_user_me_as_staff_user(self):
        self.client.login(username="staffuser1", password="password145")
        response = self.client.get(reverse("user-me"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], self.staff_user1.username)

    def test_user_me_as_superuser(self):
        self.client.login(username="superuser1", password="password189")
        response = self.client.get(reverse("user-me"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], self.superuser1.username)
