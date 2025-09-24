# python manage.py test accounts.tests.test_activation
from unittest import skip
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
            username="testuser123",
            email="testuser123@example.com",
            password="password123",
            is_active=False
        )

        self.register_url = reverse("user-list")
        self.activation_url = reverse("user-activation")
        self.resend_activation_url = reverse("user-resend-activation")


    # Send Activation
    ## 204

    def test_activation_success(self):
        uid = utils.encode_uid(self.user.pk)
        token = default_token_generator.make_token(self.user)
        activation_data = {"uid": uid, "token": token}
        response = self.client.post(self.activation_url, activation_data)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.user.refresh_from_db()
        self.assertTrue(self.user.is_active)
    
    ## 400
    ### Missing fields
    def test_activation_missing_uid_or_token(self):
        """Test d'échec d'activation avec uid ou token manquant"""
        response = self.client.post(self.activation_url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("uid", response.data)
        self.assertIn(MANDATORY_FIELD_ERROR_MESSAGE, response.data['uid'])
        self.assertIn("token", response.data)
        self.assertIn(MANDATORY_FIELD_ERROR_MESSAGE, response.data['token'])
        self.user.refresh_from_db()
        self.assertFalse(self.user.is_active)

    ### Invalid fields
    def test_activation_invalid_uid(self):
        """Test d'échec d'activation avec un uid ou un token invalides"""
        token = default_token_generator.make_token(self.user)
        response = self.client.post(self.activation_url, {"uid": "invalid_uid", "token": token})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("uid", response.data)
        self.assertIn(INVALID_USER_ERROR_MESSAGE, response.data['uid'])
        self.user.refresh_from_db()
        self.assertFalse(self.user.is_active)

    def test_activation_invalid_token(self):
        """Test d'échec d'activation avec un uid ou un token invalides"""
        uid = utils.encode_uid(self.user.pk)
        response = self.client.post(self.activation_url, {"uid": uid, "token": "invalid_token"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("token", response.data)
        self.assertIn(INVALID_TOKEN_ERROR_MESSAGE, response.data['token'])
        self.user.refresh_from_db()
        self.assertFalse(self.user.is_active)

    ## 403
    ### Already activate
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
        # TODO: email was sent

    ## 400
    ### Missing field
    def test_resend_activation_email_missing_email(self):
        """Test d'échec de renvoi d'email d'activation avec champ email manquant"""
        response = self.client.post(self.resend_activation_url, {})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("email", response.data)
        self.assertIn(MANDATORY_FIELD_ERROR_MESSAGE, response.data['email'])
        # TODO: no email was sent

    ### Invalid field
    def test_resend_activation_email_invalid_format(self):
        """Test d'échec de renvoi d'email d'activation avec un format d'email invalide"""
        response = self.client.post(self.resend_activation_url, {"email": "invalid-email-format"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(INVALID_EMAIL_ERROR_MESSAGE, response.data['email'])
        # TODO: no email was sent


    ## 204
    ### Email not found
    def test_resend_activation_unknow_email(self):
        """Test d'échec de renvoi d'email d'activation avec un format d'email invalide"""
        response = self.client.post(self.resend_activation_url, {"email": "unknown@email.com"})
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        # TODO: no email was sent


    ### Already activate
    def test_resend_activation_already_active_account(self):
        """Test d'échec d'activation pour un utilisateur déjà activé"""
        self.user.is_active = True
        self.user.save()
        response = self.client.post(self.resend_activation_url, {"email": self.user.email})
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        # TODO: no email was sent