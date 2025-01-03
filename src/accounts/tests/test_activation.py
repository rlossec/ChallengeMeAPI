# python manage.py test accounts.tests.test_activation
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator

from rest_framework.test import APITestCase
from rest_framework import status

from djoser import utils

from accounts.tests import MANDATORY_FIELD_ERROR_MESSAGE,  \
    INVALID_EMAIL_ERROR_MESSAGE, INVALID_TOKEN_ERROR_MESSAGE, INVALID_USER_ERROR_MESSAGE

User = get_user_model()


class TestActivationEndpoints(APITestCase):
    def setUp(self):
        # Création d'un utilisateur pour les tests
        self.user = User.objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password="password123",
            is_active=True
        )

        self.register_url = reverse("user-list")
        self.activation_url = reverse("user-activation")
        self.resend_activation_url = reverse("user-resend-activation")

    def test_user_registration_and_activation(self):
        """Test du workflow complet : inscription, récupération de uid/token et activation"""
        # 1. Inscription d'un nouvel utilisateur
        registration_data = {
            "username": "newuser",
            "email": "newuser@gmail.com",
            "password": "Example123?",
            "re_password": "Example123?",
        }
        self.client.post(self.register_url, registration_data)
        user = User.objects.get(username="newuser")
        # 2. Générer le `uid` et le `token` d'activation (envoyé par mail)
        uid = utils.encode_uid(user.pk)
        token = default_token_generator.make_token(user)
        # 3. Activer l'utilisateur avec les vrais uid et token
        activation_data = {"uid": uid, "token": token}
        response = self.client.post(self.activation_url, activation_data)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    # Send Activation
    ## Missing fields
    def test_activation_missing_uid_or_token(self):
        """Test d'échec d'activation avec uid ou token manquant"""
        response = self.client.post(self.activation_url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("uid", response.data)
        self.assertEqual(response.data['uid'][0], MANDATORY_FIELD_ERROR_MESSAGE)
        self.assertIn("token", response.data)
        self.assertEqual(response.data['token'][0], MANDATORY_FIELD_ERROR_MESSAGE)

    ## Invalid fields
    def test_activation_invalid_uid(self):
        """Test d'échec d'activation avec un uid ou un token invalides"""
        token = default_token_generator.make_token(self.user)
        response = self.client.post(self.activation_url, {"uid": "invalid_uid", "token": token})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("uid", response.data)
        self.assertEqual(response.data['uid'][0], INVALID_USER_ERROR_MESSAGE)

    def test_activation_invalid_token(self):
        """Test d'échec d'activation avec un uid ou un token invalides"""
        uid = utils.encode_uid(self.user.pk)
        response = self.client.post(self.activation_url, {"uid": uid, "token": "invalid_token"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("token", response.data)
        self.assertEqual(response.data['token'][0], INVALID_TOKEN_ERROR_MESSAGE)

    # Already activate
    def test_activation_already_active_account(self):
        """Test d'échec d'activation pour un utilisateur déjà activé"""
        self.user.is_active = True
        self.user.save()
        uid = utils.encode_uid(self.user.pk)
        token = default_token_generator.make_token(self.user)
        response = self.client.post(self.activation_url, {"uid": uid, "token": token})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIn("detail", response.data)
        self.assertEqual(response.data['detail'], "Stale token for given user.")

    # Resend Activation
    def test_resend_activation_email_successful(self):
        """Test de renvoi d'email d'activation avec un email valide pour un compte inactif"""
        response = self.client.post(self.resend_activation_url, {"email": self.user.email})
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    ## Missing field
    def test_resend_activation_email_missing_email(self):
        """Test d'échec de renvoi d'email d'activation avec champ email manquant"""
        response = self.client.post(self.resend_activation_url, {})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("email", response.data)
        self.assertEqual(response.data['email'][0], MANDATORY_FIELD_ERROR_MESSAGE)

    ## Invalid field
    def test_resend_activation_email_invalid_format(self):
        """Test d'échec de renvoi d'email d'activation avec un format d'email invalide"""
        response = self.client.post(self.resend_activation_url, {"email": "invalid-email-format"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['email'][0], INVALID_EMAIL_ERROR_MESSAGE)

    ## Email not found
    def test_resend_activation_unknow_email(self):
        """Test d'échec de renvoi d'email d'activation avec un format d'email invalide"""
        response = self.client.post(self.resend_activation_url, {"email": "unknown@email.com"})
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    # Already activate
    def test_resend_activation_already_active_account(self):
        """Test d'échec d'activation pour un utilisateur déjà activé"""
        self.user.is_active = True
        self.user.save()
        response = self.client.post(self.resend_activation_url, {"email": self.user.email})
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
