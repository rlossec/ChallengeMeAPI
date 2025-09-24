# python manage.py test accounts.tests.test_user_detail
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from django.urls import reverse

from rest_framework.test import APITestCase
from rest_framework import status

from accounts.tests import AUTHENTICATION_MISSING, INVALID_USER_ERROR_MESSAGE, MANDATORY_FIELD_ERROR_MESSAGE, NO_PERMISSION_ERROR_MESSAGE, NOT_FOUND_ID

User = get_user_model()


class TestUserRetrieveUser(APITestCase):
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

    # 200 Success
    def test_user_detail_success(self):
        """Un simple utilisateur ne peut pas accéder aux détails d'un autre utilisateur"""
        self.client.login(username="simpleuser", password="password12")
        response = self.client.get(reverse("user-detail", args=[self.simple_user.pk]))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('id', response.data)
        self.assertIn('username', response.data)
        self.assertEqual(response.data['username'], self.simple_user.username)
        self.assertIn('email', response.data)
        self.assertEqual(response.data['email'], self.simple_user.email)
        self.assertIn('first_name', response.data)
        self.assertEqual(response.data['first_name'], self.simple_user.first_name)
        self.assertIn('last_name', response.data)
        self.assertEqual(response.data['last_name'], self.simple_user.last_name)
        self.assertIn('avatar', response.data)
        self.assertEqual(response.data['avatar'], self.simple_user.avatar)
        self.assertNotIn('password', response.data)

    # 401
    ## Unauthenticated
    def test_get_user_unauthenticated(self):
        """Un utilisateur non authentifié ne peut pas accéder aux informations d'un utilisateur"""
        response = self.client.get(reverse("user-detail", args=[self.simple_user.pk]))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('detail', response.data)
        self.assertEqual(response.data['detail'], AUTHENTICATION_MISSING)

    # 404 Not Found
    def test_get_user_not_found_user_id(self):
        self.client.login(username="simpleuser", password="password12")
        response = self.client.get(reverse("user-detail", args=[NOT_FOUND_ID]))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn('detail', response.data)
        self.assertEqual(response.data['detail'], "No User matches the given query.")

    # Test Permission
    ## Own information
    def test_user_detail_own_information_as_simple_user(self):
        """Un simple utilisateur peut accéder à ses propres informations"""
        self.client.login(username="simpleuser", password="password12")
        response = self.client.get(reverse("user-detail", args=[self.simple_user.pk]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], self.simple_user.username)

    ## Other User
    def test_simple_user_detail_other_simple_user(self):
        """Test pour vérifier que l'utilisateur ne peut pas accéder aux détails d'un autre utilisateur"""
        self.client.login(username="simple_user1", password="password123")
        response = self.client.get(reverse("user-detail", args=[self.simple_user2.pk]))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_user_detail_as_staff_user(self):
        """Un utilisateur staff peut accéder aux détails de tout utilisateur"""
        self.client.login(username="staffuser1", password="password145")
        response = self.client.get(reverse("user-detail", args=[self.simple_user.pk]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_detail_as_superuser(self):
        """Un superutilisateur peut accéder aux détails de tout utilisateur"""
        self.client.login(username="superuser1", password="password189")
        response = self.client.get(reverse("user-detail", args=[self.staff_user1.pk]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestUserUpdate(APITestCase):
    def setUp(self):
        self.simple_user = User.objects.create_user(
            username="simpleuser",
            email="simpleuser@example.com",
            password="password12",
            first_name="Alice",
            last_name="Aton"
        )
        self.simple_user1 = User.objects.create_user(
            username="simple_user1",
            email="user1@example.com",
            password="password123",
            first_name="Bob",
            last_name="Bergman"
        )
        self.simple_user2 = User.objects.create_user(
            username="simple_user2",
            email="user2@example.com",
            password="password223",
            first_name="Charlie",
            last_name="Cole"
        )
        self.staff_user1 = User.objects.create_user(
            username="staffuser1",
            email="staffuser1@example.com",
            password="password145",
            is_staff=True,
            first_name="Doug",
            last_name="Desmond"
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

    # 200 Success
    def test_put_user_update_success(self):
        """Un utilisateur peut mettre à jour ses informations sauf le username et le password"""
        self.client.login(username="simpleuser", password="password12")
        response = self.client.put(reverse("user-detail", args=[self.simple_user.pk]), {
            "email": self.simple_user.email,
            "first_name": "UpdatedFirstName",
            "last_name": "UpdatedLastName",
            "username": "newusername"
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.simple_user.refresh_from_db()
        self.assertEqual(self.simple_user.first_name, "UpdatedFirstName")
        self.assertEqual(self.simple_user.last_name, "UpdatedLastName")
        # Unmodifiable
        self.assertEqual(self.simple_user.username, "simpleuser")

    def test_put_user_update_email_switch_inactive(self):
        """Un utilisateur peut mettre à jour son email"""
        self.client.login(username="simpleuser", password="password12")
        response = self.client.put(reverse("user-detail", args=[self.simple_user.pk]), {
            "email": "newemail@example.com"
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.simple_user.refresh_from_db()
        self.assertEqual(self.simple_user.email, "newemail@example.com")
        self.assertFalse(self.simple_user.is_active)

    def test_put_user_update_id(self):
        """Un utilisateur ne peut pas modifier son ID via PUT"""
        self.client.login(username="simpleuser", password="password12")
        response = self.client.put(reverse("user-detail", args=[self.simple_user.pk]), {
            "id": NOT_FOUND_ID,
            "email": self.simple_user.email,
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.simple_user.refresh_from_db()
        self.assertEqual(response.data['id'], self.simple_user.pk)

    def test_user_update_password(self):
        """Un utilisateur ne peut pas mettre à jour son mot de passe via PUT"""
        self.client.login(username="simpleuser", password="password12")
        response = self.client.put(reverse("user-detail", args=[self.simple_user.pk]), {
            "email": "simpleuser@example.com",
            "password": "newpassword",
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.simple_user.refresh_from_db()
        self.assertTrue(check_password("password12", self.simple_user.password))

    # 401
    ## Unauthenticated
    def test_user_update_unauthenticated(self):
        """Un utilisateur sans authentification recevra une réponse 401."""
        response = self.client.put(reverse("user-detail", args=[self.simple_user.pk]), {
            "email": "simpleuser@example.com",
            "first_name": "UpdatedFirstName",
            "last_name": "UpdatedLastName",
            "username": "newusername"
        })
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.simple_user.refresh_from_db()
        self.assertEqual(self.simple_user.first_name, "Alice")
        self.assertEqual(self.simple_user.last_name, "Aton")
        self.assertEqual(self.simple_user.username, "simpleuser")

    # 404 Not Found
    def test_user_update_unknown_user(self):
        """Un simple utilisateur ne peut pas supprimer un utilisateur inconnu."""
        self.client.login(username="simpleuser", password="password12")
        response = self.client.put(reverse("user-detail", args=[99999]), {})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # Permission
    def test_user_update_as_superuser(self):
        """Un superutilisateur ne peut pas mettre à jour les informations de tout utilisateur"""
        self.client.login(username="superuser", password="password789")
        response = self.client.put(reverse("user-detail", args=[self.staff_user1.pk]), {
            'email': 'updated_staff@example.com',
            "first_name": "UpdatedFirstName",
            "last_name": "UpdatedLastName",
            "username": "newusername"
        })
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.staff_user1.refresh_from_db()
        self.assertEqual(self.staff_user1.email, 'staffuser1@example.com')
        self.assertEqual(self.staff_user1.first_name, "Doug")
        self.assertEqual(self.staff_user1.last_name, "Desmond")
        self.assertEqual(self.staff_user1.username, "staffuser1")


class TestUserPatch(APITestCase):
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

    def test_patch_user_update_success(self):
        """Un utilisateur peut mettre à jour partiellement ses informations"""
        self.client.login(username="simpleuser", password="password12")
        response = self.client.patch(reverse("user-detail", args=[self.simple_user.pk]), {
            "first_name": "UpdatedFirstName"
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.simple_user.refresh_from_db()
        self.assertEqual(self.simple_user.first_name, "UpdatedFirstName")

    def test_patch_user_update_username(self):
        """Un utilisateur ne peut pas mettre à jour son nom d'utilisateur avec ce endpoint"""
        self.client.login(username="simpleuser", password="password12")
        response = self.client.patch(reverse("user-detail", args=[self.simple_user.pk]), {
            "username": "newusername"
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.simple_user.username, "simpleuser")

    def test_patch_user_update_password(self):
        """Un utilisateur ne peut pas mettre à jour son mot de passe avec ce endpoint"""
        self.client.login(username="simpleuser", password="password12")
        response = self.client.patch(reverse("user-detail", args=[self.simple_user.pk]), {
            "password": "newpassword"
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.simple_user.refresh_from_db()
        self.assertTrue(check_password("password12", self.simple_user.password))

    def test_patch_user_update_email(self):
        """Un utilisateur peut mettre à jour son email avec ce endpoint"""
        self.client.login(username="simpleuser", password="password12")
        response = self.client.patch(reverse("user-detail", args=[self.simple_user.pk]), {
            "email": "newemail@example.com"
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.simple_user.refresh_from_db()
        self.assertEqual(self.simple_user.email, "newemail@example.com")
        self.assertFalse(self.simple_user.is_active)


class TestUserDelete(APITestCase):
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

    # Success
    def test_user_delete_own_account_with_password(self):
        """Un simple utilisateur peut supprimer son propre compte avec mot de passe actuel"""
        self.client.login(username="simpleuser", password="password12")
        response = self.client.delete(reverse("user-detail", args=[self.simple_user.pk]), {
            'current_password': 'password12',
        })
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(User.objects.filter(pk=self.simple_user.pk).exists())

    # 401 Unauthenticated
    def test_user_delete_unauthenticated(self):
        """Un utilisateur sans authentification recevra une réponse 401."""
        response = self.client.delete(reverse("user-detail", args=[self.simple_user.pk]), {
            'current_password': 'password12'
        })
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # 404 Not Found
    def test_user_delete_unknown_user(self):
        """Un simple utilisateur ne peut pas supprimer un utilisateur inconnu."""
        self.client.login(username="simpleuser", password="password12")
        response = self.client.delete(reverse("user-detail", args=[99999]), {
            'current_password': 'password12'
        })
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # Permission
    def test_user_delete_own_account_without_password(self):
        """Un simple utilisateur ne peut supprimer son propre compte sans mot de passe actuel"""
        self.client.login(username="simpleuser", password="password12")
        response = self.client.delete(reverse("user-detail", args=[self.simple_user.pk]), {})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("current_password", response.data)
        self.assertEqual(response.data["current_password"][0], MANDATORY_FIELD_ERROR_MESSAGE)
        self.assertTrue(User.objects.filter(pk=self.simple_user.pk).exists())

    def test_user_delete_simple_user_with_password(self):
        """Un simple utilisateur ne peut pas supprimer le compte d'un autre simple utilisateur"""
        self.client.login(username="simpleuser", password="password12")
        response = self.client.delete(reverse("user-detail", args=[self.simple_user2.pk]), {
            'current_password': 'password12'
        })
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIn("detail", response.data)
        self.assertEqual(response.data["detail"], NO_PERMISSION_ERROR_MESSAGE)
        self.assertTrue(User.objects.filter(pk=self.simple_user2.pk).exists())

    def test_user_delete_other_simple_user_without_password(self):
        """Un simple utilisateur ne peut pas supprimer le compte d'un autre simple utilisateur"""
        self.client.login(username="simpleuser", password="password12")
        response = self.client.delete(reverse("user-detail", args=[self.simple_user2.pk]), {})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(User.objects.filter(pk=self.simple_user2.pk).exists())

    ## Staff user / superuser
    def test_staff_user_delete_simple_user_with_password(self):
        """Un utilisateur staff peut supprimer le compte d'un simple utilisateur avec son propre mot de passe"""
        self.client.login(username="staffuser1", password="password145")
        response = self.client.delete(reverse("user-detail", args=[self.simple_user.pk]), {
            'current_password': 'password145'
        })
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(User.objects.filter(pk=self.simple_user.pk).exists())

    def test_staff_user_delete_simple_user_without_password(self):
        """Un utilisateur staff ne peut pas supprimer le compte d'un simple utilisateur sans le mot de passe actuel"""
        self.client.login(username="staffuser1", password="password145")
        response = self.client.delete(reverse("user-detail", args=[self.simple_user.pk]), {})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue(User.objects.filter(pk=self.simple_user.pk).exists())

    def test_staff_user_delete_staff_user_with_password(self):
        """Un utilisateur staff peut supprimer un autre utilisateur staff avec le mot de passe actuel"""
        self.client.login(username="staffuser1", password="password145")
        response = self.client.delete(reverse("user-detail", args=[self.staff_user2.pk]), {
            'current_password': 'password145'
        })
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(User.objects.filter(pk=self.staff_user2.pk).exists())

    def test_staff_user_delete_staff_user_without_password(self):
        """Un utilisateur staff ne peut pas supprimer un autre utilisateur staff sans son propre mot de passe"""
        self.client.login(username="staffuser1", password="password145")
        response = self.client.delete(reverse("user-detail", args=[self.staff_user2.pk]))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue(User.objects.filter(pk=self.staff_user2.pk).exists())

    def test_superuser_delete_staff_user_with_password(self):
        """Un superutilisateur peut supprimer le compte d'un utilisateur staff avec son propre mot de passe"""
        self.client.login(username="superuser1", password="password189")
        response = self.client.delete(reverse("user-detail", args=[self.staff_user1.pk]), {
            'current_password': 'password189'
        })
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(User.objects.filter(pk=self.staff_user1.pk).exists())

    def test_superuser_delete_staff_user_without_password(self):
        """Un superutilisateur ne peut pas supprimer le compte d'un utilisateur staff sans le mot de passe actuel"""
        self.client.login(username="superuser1", password="password189")
        response = self.client.delete(reverse("user-detail", args=[self.staff_user1.pk]), {})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue(User.objects.filter(pk=self.staff_user1.pk).exists())

    def test_staff_user_delete_superuser(self):
        """Un utilisateur staff peut supprimer un superutilisateur avec son propre mot de passe."""
        self.client.login(username="staffuser1", password="password145")
        response = self.client.delete(reverse("user-detail", args=[self.superuser1.pk]), {
            'current_password': 'password145'
        })
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(User.objects.filter(pk=self.superuser1.pk).exists())

    def test_superuser_delete_another_superuser(self):
        """Un superutilisateur peut supprimer un autre superutilisateur avec son propre mot de passe."""
        self.client.login(username="superuser1", password="password189")
        response = self.client.delete(reverse("user-detail", args=[self.superuser2.pk]), {
            'current_password': 'password189'
        })
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(User.objects.filter(pk=self.superuser2.pk).exists())

    def test_staff_user_delete_unknown_user(self):
        """Un utilisateur staff ne peut pas supprimer un utilisateur inconnu."""
        self.client.login(username="staffuser1", password="password145")
        response = self.client.delete(reverse("user-detail", args=[99999]), {
            'current_password': 'password145'
        })
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_superuser_delete_unknown_user(self):
        """Un superutilisateur ne peut pas supprimer un utilisateur inconnu."""
        self.client.login(username="superuser1", password="password189")
        response = self.client.delete(reverse("user-detail", args=[99999]), {
            'current_password': 'password189'
        })
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
