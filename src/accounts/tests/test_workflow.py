# python manage.py test accounts.tests.test_workflow
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator

from rest_framework.test import APITestCase
from rest_framework import status

from djoser import utils

User = get_user_model()


class TestRegisterAndActivationWorkflow(APITestCase):
    def setUp(self):
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

