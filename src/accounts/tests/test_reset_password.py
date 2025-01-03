# python manage.py test accounts.tests.test_reset_password
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator

from rest_framework.test import APITestCase
from rest_framework import status

from djoser import utils

from accounts.tests import MANDATORY_FIELD_ERROR_MESSAGE, \
    INVALID_EMAIL_ERROR_MESSAGE, INVALID_USER_ERROR_MESSAGE, INVALID_TOKEN_ERROR_MESSAGE, \
    PASSWORD_TOO_SHORT_ERROR_MESSAGE

User = get_user_model()


class TestResetPasswordEndpoints(APITestCase):
    def setUp(self):
        # Création de l'utilisateur de test
        self.user = User.objects.create_user(
            username="testuser",
            email="user@example.com",
            password="oldpassword"
        )

        # URLs pour les endpoints
        self.reset_password_url = reverse("user-reset-password")
        self.reset_password_confirm_url = reverse("user-reset-password-confirm")

    # Reset
    def test_reset_password_success(self):
        """Envoie une demande de réinitialisation de mot de passe avec un email valide"""
        response = self.client.post(self.reset_password_url, {"email": "user@example.com"})
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        # Tentative de connexion avec l'ancien mot de passe
        login_response = self.client.login(email="user@example.com", password="oldpassword")
        self.assertFalse(login_response)

    ## Missing field
    def test_reset_password_with_missing_email(self):
        """Vérifie que le champ 'email' est obligatoire pour la demande de réinitialisation du mot de passe"""
        response = self.client.post(self.reset_password_url, {})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("email", response.data)
        self.assertEqual(response.data["email"][0], MANDATORY_FIELD_ERROR_MESSAGE)

    ## Invalid email
    def test_reset_password_with_invalid_email(self):
        """Vérifie que le champ 'email' est valide pour la demande de réinitialisation du mot de passe"""
        response = self.client.post(self.reset_password_url, {"email": "invalid_mail"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("email", response.data)
        self.assertEqual(response.data["email"][0], INVALID_EMAIL_ERROR_MESSAGE)

    # Reset confirm
    def test_reset_password_confirm_success(self):
        """Confirme la réinitialisation du mot de passe avec des valeurs UID et token valides"""
        uid = utils.encode_uid(self.user.pk)
        token = default_token_generator.make_token(self.user)
        response = self.client.post(self.reset_password_confirm_url, {
            "uid": uid,
            "token": token,
            "new_password": "newpassword123"
        })
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        # Vérifie que le mot de passe a bien été mis à jour
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password("newpassword123"))

    ## Missing fields
    def test_reset_password_confirm_with_missing_fields(self):
        """Vérifie que les champs 'uid', 'token' et 'new_password' sont obligatoires pour confirmer la réinitialisation"""
        response = self.client.post(self.reset_password_confirm_url, {})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("uid", response.data)
        self.assertIn("token", response.data)
        self.assertIn("new_password", response.data)
        self.assertEqual(response.data["uid"][0], MANDATORY_FIELD_ERROR_MESSAGE)
        self.assertEqual(response.data["token"][0], MANDATORY_FIELD_ERROR_MESSAGE)
        self.assertEqual(response.data["new_password"][0], MANDATORY_FIELD_ERROR_MESSAGE)

    ## Invalid fields
    def test_reset_password_confirm_invalid_uid(self):
        """Vérifie le message d'erreur pour un UID invalide lors de la confirmation"""
        invalid_uid = utils.encode_uid(9999)  # UID d'un utilisateur inexistant
        token = default_token_generator.make_token(self.user)
        response = self.client.post(self.reset_password_confirm_url, {
            "uid": invalid_uid,
            "token": token,
            "new_password": "newpassword123"
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("uid", response.data)
        self.assertEqual(response.data["uid"][0], INVALID_USER_ERROR_MESSAGE)

    def test_reset_password_confirm_invalid_token(self):
        """Vérifie le message d'erreur pour un token invalide lors de la confirmation"""
        uid = utils.encode_uid(self.user.pk)
        invalid_token = "invalid-token"
        response = self.client.post(self.reset_password_confirm_url, {
            "uid": uid,
            "token": invalid_token,
            "new_password": "newpassword123"
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("token", response.data)
        self.assertEqual(response.data["token"][0], INVALID_TOKEN_ERROR_MESSAGE)

    def test_reset_password_confirm_with_expired_token(self):
        """Vérifie le comportement si le token de réinitialisation est expiré"""
        uid = utils.encode_uid(self.user.pk)
        expired_token = "expired-token"  # Utilisez une méthode appropriée pour générer un token expiré
        response = self.client.post(self.reset_password_confirm_url, {
            "uid": uid,
            "token": expired_token,
            "new_password": "newpassword123"
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("token", response.data)
        self.assertEqual(response.data["token"][0], INVALID_TOKEN_ERROR_MESSAGE)

    def test_reset_password_confirm_with_weak_password(self):
        """Vérifie que le 'new_password' respecte les règles de complexité (ex. longueur minimale)"""
        uid = utils.encode_uid(self.user.pk)
        token = default_token_generator.make_token(self.user)

        response = self.client.post(self.reset_password_confirm_url, {
            "uid": uid,
            "token": token,
            "new_password": "123"
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("new_password", response.data)
        self.assertEqual(response.data["new_password"][0], PASSWORD_TOO_SHORT_ERROR_MESSAGE)
