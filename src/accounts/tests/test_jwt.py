# python manage.py test accounts.tests.test_jwt
from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework.test import APITestCase
from rest_framework import status

from accounts.tests import MANDATORY_FIELD_ERROR_MESSAGE, EXPIRED_TOKEN_ERROR_MESSAGE, \
    INVALID_CREDENTIALS_ERROR_MESSAGE

User = get_user_model()


class TestJWTEndpoints(APITestCase):
    def setUp(self):
        # Créer un utilisateur actif pour les tests
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='password123'
        )
        # Créer un utilisateur inactif pour le test d'inactivité
        self.inactive_user = User.objects.create_user(
            username='inactiveuser',
            email='inactiveuser@example.com',
            password='password123',
            is_active=False
        )
        # URLs des endpoints JWT
        self.jwt_create_url = reverse('jwt-create')
        self.jwt_refresh_url = reverse('jwt-refresh')
        self.jwt_verify_url = reverse('jwt-verify')

    def test_jwt_create(self):
        """Test pour vérifier la génération du token JWT avec des identifiants valides"""
        response = self.client.post(self.jwt_create_url, {
            'username': 'testuser',
            'password': 'password123'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_jwt_create_inactive_user(self):
        """Test pour vérifier qu'un utilisateur inactif ne peut pas générer de token JWT"""
        response = self.client.post(self.jwt_create_url, {
            'username': 'inactiveuser',
            'password': 'password123'
        })
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('detail', response.data)
        self.assertEqual(response.data['detail'], INVALID_CREDENTIALS_ERROR_MESSAGE)

    def test_jwt_create_invalid_credentials(self):
        """Test pour vérifier que des identifiants invalides ne génèrent pas de token"""
        response = self.client.post(self.jwt_create_url, {
            'username': 'testuser',
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('detail', response.data)
        self.assertEqual(response.data['detail'], INVALID_CREDENTIALS_ERROR_MESSAGE)
        self.assertNotIn('access', response.data)
        self.assertNotIn('refresh', response.data)

    def test_jwt_create_missing_fields(self):
        """Test pour vérifier les erreurs de champs manquants pour jwt-create"""
        response = self.client.post(self.jwt_create_url, {'username': 'testuser'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('password', response.data)
        self.assertEqual(response.data['password'][0], MANDATORY_FIELD_ERROR_MESSAGE)

        response = self.client.post(self.jwt_create_url, {'password': 'password123'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('username', response.data)
        self.assertEqual(response.data['username'][0], MANDATORY_FIELD_ERROR_MESSAGE)

    # Refresh
    def test_jwt_refresh(self):
        """Test pour vérifier le rafraîchissement du token JWT"""
        # Générer un token avec des identifiants valides
        response = self.client.post(self.jwt_create_url, {
            'username': 'testuser',
            'password': 'password123'
        })
        refresh_token = response.data['refresh']
        # Rafraîchir le token
        response = self.client.post(self.jwt_refresh_url, {'refresh': refresh_token})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)

    def test_jwt_refresh_missing_field(self):
        """Test pour vérifier l'erreur de champ manquant pour jwt-refresh"""
        response = self.client.post(self.jwt_refresh_url, {})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('refresh', response.data)
        self.assertEqual(response.data['refresh'][0], MANDATORY_FIELD_ERROR_MESSAGE)

    def test_jwt_refresh_invalid_token(self):
        """Test pour vérifier l'erreur de champ manquant pour jwt-refresh"""
        response = self.client.post(self.jwt_refresh_url, {'refresh': "invalid_token"})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('detail', response.data)
        self.assertEqual(response.data['detail'], EXPIRED_TOKEN_ERROR_MESSAGE)
        self.assertIn('code', response.data)
        self.assertEqual(response.data['code'], 'token_not_valid')

    # Verify
    def test_jwt_verify(self):
        """Test pour vérifier la validité du token JWT"""
        # Générer un token avec des identifiants valides
        response = self.client.post(self.jwt_create_url, {
            'username': 'testuser',
            'password': 'password123'
        })
        access_token = response.data['access']
        # Vérifier le token d'accès
        response = self.client.post(self.jwt_verify_url, {'token': access_token})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual({}, response.data)

    def test_jwt_verify_invalid_token(self):
        """Test pour vérifier qu'un token JWT invalide ne passe pas la vérification"""
        invalid_token = 'abc123'  # Faux token
        response = self.client.post(self.jwt_verify_url, {'token': invalid_token})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('detail', response.data)
        self.assertEqual(response.data['detail'], EXPIRED_TOKEN_ERROR_MESSAGE)
        self.assertIn('code', response.data)
        self.assertEqual(response.data['code'], 'token_not_valid')

    def test_jwt_verify_missing_field(self):
        """Test pour vérifier l'erreur de champ manquant pour jwt-verify"""
        response = self.client.post(self.jwt_verify_url, {})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('token', response.data)
        self.assertEqual(response.data['token'][0], MANDATORY_FIELD_ERROR_MESSAGE)

    def test_jwt_tokens_validity(self):
        """Test pour vérifier que les tokens sont valides"""
        # Créer un token JWT
        response = self.client.post(self.jwt_create_url, {
            'username': 'testuser',
            'password': 'password123'
        })
        access_token = response.data['access']
        refresh_token = response.data['refresh']
        # Vérifier les tokens
        response = self.client.post(self.jwt_verify_url, {'token': access_token})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Rafraîchir le token
        response = self.client.post(self.jwt_refresh_url, {'refresh': refresh_token})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
