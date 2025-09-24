# python manage.py test accounts.tests.test_user_me

from pathlib import Path


from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.test import APITestCase

from accounts.tests.utils.generate_image import generate_test_image
from accounts.tests import AUTHENTICATION_MISSING, MANDATORY_FIELD_ERROR_MESSAGE, \
    INVALID_EMAIL_ERROR_MESSAGE, EMAIL_ALREADY_TAKEN_ERROR_MESSAGE, \
    NOT_FOUND_ID, FIELD_TOO_LONG_ERROR_MESSAGE

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
        self.assertIn('username', response.data)
        self.assertEqual(response.data['username'], self.user.username)
        self.assertIn('email', response.data)
        self.assertEqual(response.data['email'], self.user.email)
        self.assertIn('first_name', response.data)
        self.assertEqual(response.data['first_name'], self.user.first_name)
        self.assertIn('last_name', response.data)
        self.assertEqual(response.data['last_name'], self.user.last_name)
        self.assertIn('avatar', response.data)
        self.assertEqual(response.data['avatar'], self.user.avatar)
        # Excluded fields
        self.assertNotIn('password', response.data)

    ## Unauthenticated
    def test_get_user_me_without_authentication(self):
        response = self.client.get(self.user_me_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('detail', response.data)
        self.assertEqual(response.data['detail'], AUTHENTICATION_MISSING)
        self.assertNotIn('username', response.data)

    # Update
    ## 200 Success
    def test_put_user_me(self):
        """Test pour mettre à jour les informations de l'utilisateur (sans changer le nom d'utilisateur)"""
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        response = self.client.put(self.user_me_url, {
            'id': NOT_FOUND_ID,
            'username': 'newusername',
            'email': 'newemail@example.com',
            'first_name': 'Pau',
            'last_name': 'Gasol'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        # Unmodifiable
        self.assertNotEqual(self.user.id, NOT_FOUND_ID)
        self.assertEqual(response.data['username'], self.user.username)
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
            "email": self.user.email,
            'username': 'newusername'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, 'testuser')
        self.assertEqual(response.data['username'], self.user.username)

    ## 401 Unauthenticated
    def test_put_user_me_without_authentication(self):
        response = self.client.put(self.user_me_url, {'email': 'unauthenticated@example.com'})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('detail', response.data)
        self.assertEqual(response.data['detail'], AUTHENTICATION_MISSING)

    ## 400 
    ### Missing fields
    def test_put_user_me_missing_email(self):
        """Test pour vérifier que la mise à jour échoue avec des champs manquants"""
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        response = self.client.put(self.user_me_url, {
            'first_name': 'Pau',
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data)
        self.assertEqual(response.data['email'][0], MANDATORY_FIELD_ERROR_MESSAGE)
        self.assertEqual(self.user.first_name, 'John')

    ### Invalid field
    def test_put_user_me_first_name_too_long(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        response = self.client.put(self.user_me_url, {'first_name': 'a' * 151})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('first_name', response.data)
        self.assertIn(FIELD_TOO_LONG_ERROR_MESSAGE, response.data['first_name'])

    def test_put_user_me_last_name_too_long(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        response = self.client.put(self.user_me_url, {'last_name': 'a' * 151})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('last_name', response.data)
        self.assertIn(FIELD_TOO_LONG_ERROR_MESSAGE, response.data['last_name'])

    
    def test_put_user_me_invalid_email_format(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        response = self.client.put(self.user_me_url, {'email': 'notanemail'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data)
        self.assertIn(INVALID_EMAIL_ERROR_MESSAGE, response.data['email'])
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
        self.assertIn(EMAIL_ALREADY_TAKEN_ERROR_MESSAGE, response.data['email'])
        self.assertTrue(self.user.is_active)

    # Partial update
    ## Success
    def test_patch_user_me(self):
        """Test pour mettre à jour partiellement les informations de l'utilisateur (sans changer le nom d'utilisateur)"""
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        response = self.client.patch(self.user_me_url, {
            'id': NOT_FOUND_ID,
            'username': 'newusername',
            'email': 'newemail@example.com',
            'first_name': 'Pau',
            'last_name': 'Gasol'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        # Unmodifiable
        self.assertNotEqual(self.user.id, NOT_FOUND_ID)
        self.assertEqual(self.user.username, 'testuser')
        self.assertEqual(response.data['username'], self.user.username)
        # Modifications
        self.assertEqual(self.user.first_name, 'Pau')
        self.assertEqual(response.data['first_name'], 'Pau')
        self.assertEqual(self.user.last_name, 'Gasol')
        self.assertEqual(response.data['last_name'], 'Gasol')

        self.assertEqual(self.user.email, 'newemail@example.com')
        self.assertEqual(response.data['email'], 'newemail@example.com')
        self.assertFalse(self.user.is_active)

    def test_patch_user_me_without_email(self):
        """Test pour vérifier que la mise à jour réussi sans email"""
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        response = self.client.patch(self.user_me_url, {
            'first_name': 'Pau',
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.user.first_name, 'John')

    ## 401 
    ### Unauthenticated
    def test_patch_user_me_without_authentication(self):
        response = self.client.patch(self.user_me_url, {'email': 'unauthenticated@example.com'})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('detail', response.data)
        self.assertEqual(response.data['detail'], AUTHENTICATION_MISSING)

    ## 400 
    ### Invalid field
    def test_patch_user_me_first_name_too_long(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        response = self.client.patch(self.user_me_url, {'first_name': 'a' * 151})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('first_name', response.data)
        self.assertIn(FIELD_TOO_LONG_ERROR_MESSAGE, response.data['first_name'])

    def test_patch_user_me_last_name_too_long(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        response = self.client.patch(self.user_me_url, {'last_name': 'a' * 151})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('last_name', response.data)
        self.assertIn(FIELD_TOO_LONG_ERROR_MESSAGE, response.data['last_name'])

    def test_patch_user_me_invalid_email_format(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        response = self.client.patch(self.user_me_url, {'email': 'notanemail'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data)
        self.assertIn(INVALID_EMAIL_ERROR_MESSAGE, response.data['email'])
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
        self.assertIn(EMAIL_ALREADY_TAKEN_ERROR_MESSAGE, response.data['email'])
        self.assertTrue(self.user.is_active)

    # Delete
    def test_delete_user_me_success(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        response = self.client.delete(self.user_me_url, {'current_password': 'ValidPassword123!'})
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        # Vérifier que l'utilisateur est supprimé
        self.assertFalse(User.objects.filter(id=self.user.id).exists())

    ## 401 
    ### Unauthenticated
    def test_delete_user_me_unauthenticated(self):
        response = self.client.delete(self.user_me_url, {'current_password': 'ValidPassword123!'})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('detail', response.data)
        self.assertEqual(response.data['detail'], AUTHENTICATION_MISSING)

    def test_delete_user_me_already_deleted(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.user.delete()
        response = self.client.delete(self.user_me_url, {'current_password': 'ValidPassword123!'})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('detail', response.data)
        self.assertEqual(response.data['detail'], "User not found")
        self.assertEqual(response.data['code'], 'user_not_found')

    ## 400 
    ### Missing field
    def test_delete_user_me_without_password(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        response = self.client.delete(self.user_me_url, {})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('current_password', response.data)
        self.assertIn(MANDATORY_FIELD_ERROR_MESSAGE, response.data['current_password'])


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


class TestUserAvatarUpdate(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='ValidPassword123!',
            first_name='John',
            last_name='Doe',
            avatar=generate_test_image('old_avatar.jpg')
        )
        self.token = self.client.post(reverse('jwt-create'), {
            'username': 'testuser',
            'password': 'ValidPassword123!'
        }).data['access']
        self.user_me_url = reverse('user-me')

    def test_update_avatar_removes_old_file(self):
        """Test que la mise à jour du champ avatar supprime l'ancien fichier."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')

        # Vérifier que l'ancien fichier existe
        old_avatar_path = Path(self.user.avatar.path)
        self.assertTrue(old_avatar_path.exists())

        new_avatar = generate_test_image('new_avatar.jpg')
        response = self.client.patch(self.user_me_url, {'avatar': new_avatar})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()

        self.assertFalse(old_avatar_path.exists())

        self.assertIn('new_avatar.jpg', self.user.avatar.name)
        self.assertTrue(Path(self.user.avatar.path).exists())

    def tearDown(self):
        """Supprime tous les fichiers créés lors des tests."""
        avatar_path = Path(self.user.avatar.path)
        if self.user.avatar and avatar_path.exists():
            avatar_path.unlink()