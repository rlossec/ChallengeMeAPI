# python manage.py test accounts.tests.test_reset_username
from unittest import skip
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator

from rest_framework.test import APITestCase
from rest_framework import status

from djoser import utils

from accounts.tests import MANDATORY_FIELD_ERROR_MESSAGE, \
    INVALID_EMAIL_ERROR_MESSAGE, INVALID_USER_ERROR_MESSAGE, INVALID_TOKEN_ERROR_MESSAGE, \
    INVALID_USERNAME

User = get_user_model()


class TestResetUsernameEndpoints(APITestCase):
    def setUp(self):
        # Création de l'utilisateur de test
        self.user = User.objects.create_user(
            username="oldusername",
            email="user@gmail.com",
            password="Example123?"
        )

        # URLs pour les endpoints
        self.reset_username_url = reverse("user-reset-username")
        self.reset_username_confirm_url = reverse("user-reset-username-confirm")

    # Reset username
    @skip("Not implemented")
    def test_reset_username_success(self):
        """Envoie un email de réinitialisation de nom d'utilisateur avec un email valide"""
        response = self.client.post(self.reset_username_url, {"email": "user@example.com"})
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    ## Missing email
    @skip("Not implemented")
    def test_reset_username_with_missing_email(self):
        """Vérifie que le champ 'email' est obligatoire pour la demande de réinitialisation"""
        response = self.client.post(self.reset_username_url, {})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("email", response.data)
        self.assertEqual(response.data["email"][0], MANDATORY_FIELD_ERROR_MESSAGE)

    ## Invalid email
    @skip("Not implemented")
    def test_reset_username_with_invalid_email(self):
        """Vérifie que le champ 'email' est obligatoire pour la demande de réinitialisation"""
        response = self.client.post(self.reset_username_url, {"email": "invalid_email"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("email", response.data)
        self.assertEqual(response.data["email"][0], INVALID_EMAIL_ERROR_MESSAGE)

    ## Unknown email
    @skip("Not implemented")
    def test_reset_username_with_unknown_email(self):
        """Vérifie que l'erreur est renvoyée si l'email n'existe pas dans la base de données"""
        response = self.client.post(self.reset_username_url, {"email": "nonexistent_user@gmail.com"})
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    # Reset password confirm
    @skip("Not implemented")
    def test_reset_username_confirm_success(self):
        """Réinitialise le nom d'utilisateur avec des valeurs UID et token valides"""
        uid = utils.encode_uid(self.user.pk)
        token = default_token_generator.make_token(self.user)

        response = self.client.post(self.reset_username_confirm_url, {
            "uid": uid,
            "token": token,
            "new_username": "newusername"
        })
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Vérifier que le nom d'utilisateur a bien été changé
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, "newusername")

    ## Missing fields
    @skip("Not implemented")
    def test_reset_username_confirm_with_missing_new_username(self):
        """Vérifie que le champ 'new_username' est obligatoire pour confirmer la réinitialisation"""
        response = self.client.post(self.reset_username_confirm_url, {})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("new_username", response.data)
        self.assertEqual(response.data["new_username"][0], MANDATORY_FIELD_ERROR_MESSAGE)

    @skip("Not implemented")
    def test_reset_username_confirm_with_missing_uid(self):
        """Vérifie que le champ 'new_username' est obligatoire pour confirmer la réinitialisation"""
        response = self.client.post(self.reset_username_confirm_url, {"new_username": "newusername"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("uid", response.data)
        self.assertEqual(response.data["uid"][0], INVALID_USER_ERROR_MESSAGE)

    @skip("Not implemented")
    def test_reset_username_confirm_with_missing_token(self):
        """Réinitialise le nom d'utilisateur avec des valeurs UID et token valides"""
        uid = utils.encode_uid(self.user.pk)
        response = self.client.post(self.reset_username_confirm_url, {
            "uid": uid,
            "new_username": "newusername"
        })
        self.assertIn("token", response.data)
        self.assertEqual(response.data["token"][0], INVALID_TOKEN_ERROR_MESSAGE)

    # Invalid fields
    @skip("Not implemented")
    def test_reset_username_confirm_invalid_uid(self):
        """Vérifie le message d'erreur pour un UID invalide"""
        invalid_uid = utils.encode_uid(9999)  # UID d'un utilisateur inexistant
        token = default_token_generator.make_token(self.user)
        response = self.client.post(self.reset_username_confirm_url, {
            "uid": invalid_uid,
            "token": token,
            "new_username": "newusername"
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("uid", response.data)
        self.assertEqual(response.data["uid"][0], INVALID_USER_ERROR_MESSAGE)

    @skip("Not implemented")
    def test_reset_username_confirm_invalid_token(self):
        """Vérifie le message d'erreur pour un token invalide"""
        uid = utils.encode_uid(self.user.pk)
        invalid_token = "invalid-token"
        response = self.client.post(self.reset_username_confirm_url, {
            "uid": uid,
            "token": invalid_token,
            "new_username": "newusername"
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("token", response.data)
        self.assertEqual(response.data["token"][0], INVALID_TOKEN_ERROR_MESSAGE)

    @skip("Not implemented")
    def test_reset_username_confirm_with_invalid_format_username(self):
        """Vérifie que le format du 'new_username' respecte les règles de validation (caractères spéciaux, longueur)"""
        uid = utils.encode_uid(self.user.pk)
        token = default_token_generator.make_token(self.user)

        response = self.client.post(self.reset_username_confirm_url, {
            "uid": uid,
            "token": token,
            "new_username": "username_with_invalid_characters!@"
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("new_username", response.data)
        self.assertEqual(response.data["new_username"][0], INVALID_USERNAME)

    @skip("Not implemented")
    def test_reset_username_confirm_with_expired_token(self):
        """Vérifie le comportement si le token de réinitialisation est expiré"""
        uid = utils.encode_uid(self.user.pk)
        # Expire le token en utilisant un token ancien
        expired_token = "expired-token"  # À remplacer par une méthode pour créer un token expiré si possible
        response = self.client.post(self.reset_username_confirm_url, {
            "uid": uid,
            "token": expired_token,
            "new_username": "newusername"
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("token", response.data)
        self.assertEqual(response.data["token"][0], INVALID_TOKEN_ERROR_MESSAGE)
