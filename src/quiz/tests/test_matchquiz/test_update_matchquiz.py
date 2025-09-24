from unittest import skip
from typing import List, Tuple, Union, Dict

from rest_framework import status

from django.contrib.auth import get_user_model

from ...models import MatchPair
from ...tests.test_matchquiz import TestMatchQuiz

User = get_user_model()


class TestMatchQuizUpdateEndpoint(TestMatchQuiz):

    def assertPairsMatch(self, expected_pairs: List[Dict[str, Union[str, None]]], actual_pairs: List[MatchPair]) -> None:
        """Vérifie que chaque paire dans `expected_pairs` a une correspondance exacte dans `actual_pairs`."""

        def extract_pair(pair: Union[Dict[str, Union[str, None]], MatchPair]) -> Tuple[str, str]:
            """Extrait une paire sous forme de tuple (indice, réponse), que ce soit un dict ou un objet MatchPair."""
            if isinstance(pair, dict):
                clue = pair.get("text_clue") or pair.get("picture_clue")
                answer = pair.get("answer")
            else:
                clue = pair.text_clue or pair.picture_clue
                answer = pair.answer

            if clue is None or answer is None:
                raise ValueError(f"Paire invalide détectée : {pair}")

            return clue, answer
        # Vérification du nombre de paires
        self.assertEqual(len(actual_pairs), len(expected_pairs), "Le nombre de paires ne correspond pas.")
        # Transformation en ensemble pour comparaison indépendante de l'ordre
        expected_set: set[Tuple[str, str]] = {extract_pair(p) for p in expected_pairs}
        actual_set: set[Tuple[str, str]] = {extract_pair(p) for p in actual_pairs}
        self.assertSetEqual(
            actual_set, expected_set,
            f"Les paires en base ne correspondent pas aux données attendues.\nAttendu: {expected_set}\nReçu: {actual_set}"
        )

    # 401
    def test_update_match_quiz_unauthenticated(self):
        """Test pour vérifier qu'une mise à jour échoue sans authentification."""
        updated_data = {
            "title": "Unauthorized Update Title",
            "text": "Unauthorized Update Description",
            "valid": False,
            "pairs": [{"text_clue": "France", "answer": "Paris"}]
        }
        response = self.client.put(
            self.match_quiz_update_url,
            updated_data,
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.match_quiz.refresh_from_db()
        self.assertNotEqual(self.match_quiz.title, updated_data["title"])
        self.assertNotEqual(self.match_quiz.text, updated_data["text"])

    # 200
    def test_update_match_quiz_success(self):
        """Test pour vérifier qu'une mise à jour complète fonctionne avec une authentification valide."""
        self.client.force_authenticate(self.user)
        updated_data = {
            "title": "Quiz de correspondance exemple",
            "text": "Associez les indices avec leurs réponses.",
            "type": "MT",
            "difficulty": 2,
            "themes": [theme.id for theme in self.themes],
            "base_url": "http://example.com/base",
            "valid": True,
            "pairs": [
                {
                    "id": self.pairs[0].id,
                    "text_clue": "Indice texte 1 mis à jour",
                    "picture_clue": None,
                    "answer": "Réponse 1 mise à jour"
                },
                {
                    "id": self.pairs[1].id,
                    "text_clue": None,
                    "picture_clue": "image1_updated.jpg",
                    "answer": "Réponse 2 mise à jour"
                }
            ]
        }

        response = self.client.put(
            self.match_quiz_update_url,
            updated_data,
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.match_quiz.refresh_from_db()

        # Vérification des champs principaux
        self.assertEqual(self.match_quiz.title, updated_data["title"])
        self.assertEqual(self.match_quiz.text, updated_data["text"])
        self.assertEqual(self.match_quiz.valid, updated_data["valid"])
        self.assertEqual(self.match_quiz.difficulty, updated_data["difficulty"])
        self.assertEqual(self.match_quiz.base_url, updated_data["base_url"])
        # Vérification des thèmes associés
        updated_themes = list(self.match_quiz.themes.values_list("id", flat=True))
        self.assertListEqual(updated_themes, updated_data["themes"])
        # Vérification des paires mises à jour
        updated_pairs = list(self.match_quiz.pairs.all())
        self.assertPairsMatch(updated_data["pairs"], updated_pairs)

    def test_update_match_quiz_with_themes_and_pairs(self):
        """Test de mise à jour avec des thèmes et des paires ajoutés."""
        self.client.force_authenticate(self.user)
        updated_data = {
            "title": "Updated Quiz Title",
            "text": "Updated Quiz Description",
            "type": "MT",
            "difficulty": "3",
            "themes": [theme.id for theme in self.themes],
            "pairs": [
                {"text_clue": "Indice mis à jour", "answer": "Nouvelle réponse"},
                {"text_clue": "Nouveau Indice", "answer": "Nouvelle Réponse"},
            ]
        }
        response = self.client.put(
            self.match_quiz_update_url,
            updated_data,
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.match_quiz.refresh_from_db()
        self.assertEqual(self.match_quiz.title, updated_data["title"])
        self.assertEqual(self.match_quiz.text, updated_data["text"])
        self.assertEqual(self.match_quiz.difficulty, float(updated_data["difficulty"]))
        self.assertEqual(list(self.match_quiz.themes.all()), self.themes)
        updated_pairs = list(self.match_quiz.pairs.all())
        self.assertPairsMatch(updated_data["pairs"], updated_pairs)

    def test_update_match_quiz_remove_pairs(self):
        """Vérifier que les paires sont supprimées si non présentes dans `pairs`."""
        self.client.force_authenticate(self.user)

        updated_data = {
            "title": "Quiz mis à jour",
            "text": "Texte mise à jour",
            "pairs": [
                {"text_clue": "Indice 1 modifié", "answer": "Réponse 1 modifiée"}
            ]
        }

        response = self.client.put(
            self.match_quiz_update_url,
            updated_data,
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.match_quiz.refresh_from_db()
        updated_pairs = list(self.match_quiz.pairs.all())
        self.assertPairsMatch(updated_data["pairs"], updated_pairs)

    def test_update_match_quiz_deduplicate_pairs(self):
        """Vérifier qu'une mise à jour ne crée pas de doublons dans les paires."""
        self.client.force_authenticate(self.user)
        updated_data = {
            "title": "Quiz mis à jour",
            "text": "Texte mise à jour",
            "pairs": [
                {"text_clue": "Indice 1", "answer": "Réponse 1"},
                {"text_clue": "Indice 1", "answer": "Réponse 1"}  # Doublon
            ]
        }
        response = self.client.put(
            self.match_quiz_update_url,
            updated_data,
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.match_quiz.refresh_from_db()

        self.assertEqual(self.match_quiz.pairs.count(), 1)
        updated_pairs = list(self.match_quiz.pairs.all())
        self.assertPairsMatch([{"text_clue": "Indice 1", "answer": "Réponse 1"}], updated_pairs)

    def test_update_match_quiz_with_empty_pairs(self):
        """Vérifier qu'un envoi de `pairs` vide supprime toutes les paires existantes."""
        self.client.force_authenticate(self.user)
        updated_data = {
            "title": "Titre mis à jour",
            "text": "Texte mis à jour",
            "pairs": []
        }
        response = self.client.put(
            self.match_quiz_update_url,
            updated_data,
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.match_quiz.refresh_from_db()
        updated_pairs = list(self.match_quiz.pairs.all())
        self.assertPairsMatch(updated_data["pairs"], updated_pairs)

    # 400 Missing fields
    def test_update_match_quiz_missing_title(self):
        """Vérifier qu'une requête sans `title` renvoie une erreur 400 et que le quiz reste inchangé."""
        self.client.force_authenticate(self.user)
        initial_title = self.match_quiz.title
        initial_text = self.match_quiz.text
        initial_pairs = list(self.match_quiz.pairs.all())
        updated_data = {
            # "title": "Titre mis à jour",  # Oublié intentionnellement
            "text": "Texte mis à jour",
            "pairs": [
                {"text_clue": "Indice 1", "answer": "Réponse 1"},
                {"text_clue": "Indice 1", "answer": "Réponse 1"}  # Doublon
            ]
        }
        response = self.client.put(
            self.match_quiz_update_url,
            updated_data,
            format="json"
        )
        # Vérification du statut
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # Vérification du contenu de la réponse
        self.assertIn("title", response.data)
        self.assertEqual(response.data["title"][0], "This field is required.")
        # Vérification que rien n'a été modifié en base
        self.match_quiz.refresh_from_db()
        self.assertEqual(self.match_quiz.title, initial_title, "Le titre a été modifié alors qu'il ne devait pas l'être.")
        self.assertEqual(self.match_quiz.text, initial_text, "Le texte a été modifié alors qu'il ne devait pas l'être.")
        updated_pairs = list(self.match_quiz.pairs.all())
        self.assertPairsMatch(initial_pairs, updated_pairs)

    def test_update_match_quiz_missing_text(self):
        """Vérifier que si le champ `text` est absent, on reçoit un 400 avec le champ manquant."""
        self.client.force_authenticate(self.user)
        initial_title = self.match_quiz.title
        initial_text = self.match_quiz.text
        initial_pairs = list(self.match_quiz.pairs.all())
        updated_data = {
            "title": "Titre mis à jour",
            # "text": "Texte mis à jour",
            "pairs": [
                {"text_clue": "Indice 1", "answer": "Réponse 1"},
                {"text_clue": "Indice 1", "answer": "Réponse 1"}  # Doublon
            ]
        }
        response = self.client.put(
            self.match_quiz_update_url,
            updated_data,
            format="json"
        )
        # Statut
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # Contenu de la réponse
        self.assertIn("text", response.data)
        self.assertEqual(response.data["text"][0], "This field is required.")
        self.match_quiz.refresh_from_db()
        self.assertEqual(self.match_quiz.title, initial_title, "Le titre a été modifié alors qu'il ne devait pas l'être.")
        self.assertEqual(self.match_quiz.text, initial_text, "Le texte a été modifié alors qu'il ne devait pas l'être.")
        updated_pairs = list(self.match_quiz.pairs.all())
        self.assertPairsMatch(initial_pairs, updated_pairs)

    def test_update_match_quiz_missing_pairs(self):
        """Vérifier que si le champ `pairs` est absent, les paires restent inchangées."""
        self.client.force_authenticate(self.user)
        initial_title = self.match_quiz.title
        initial_text = self.match_quiz.text
        initial_pairs = list(self.match_quiz.pairs.all())
        updated_data = {
            "title": "Titre mis à jour",
            "text": "Texte mis à jour"
            # Pas de champ "pairs"
        }
        response = self.client.put(
            self.match_quiz_update_url,
            updated_data,
            format="json"
        )
        # Statut
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # Contenu de la réponse
        self.assertIn("pairs", response.data)
        self.assertEqual(response.data["pairs"][0], "This field is required.")
        self.match_quiz.refresh_from_db()
        # Vérifier que dans la réponse on obtient bien en clé le champ manquant avec l'information qu'il est requis
        self.match_quiz.refresh_from_db()
        self.assertEqual(self.match_quiz.title, initial_title, "Le titre a été modifié alors qu'il ne devait pas l'être.")
        self.assertEqual(self.match_quiz.text, initial_text, "Le texte a été modifié alors qu'il ne devait pas l'être.")
        updated_pairs = list(self.match_quiz.pairs.all())
        self.assertPairsMatch(initial_pairs, updated_pairs)

    # 400 Invalid data
    def test_update_match_quiz_invalid_data(self):
        """Test pour vérifier qu'une mise à jour échoue avec des données invalides."""
        self.client.force_authenticate(self.user)
        initial_title = self.match_quiz.title
        initial_text = self.match_quiz.text
        initial_pairs = list(self.match_quiz.pairs.all())
        updated_data = {
            "title": "",
            "text": "Updated Description",

        }
        response = self.client.put(
            self.match_quiz_update_url,
            updated_data,
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("title", response.data)
        self.assertEqual(response.data["title"][0], 'This field may not be blank.')
        self.match_quiz.refresh_from_db()
        self.match_quiz.refresh_from_db()
        self.assertEqual(self.match_quiz.title, initial_title, "Le titre a été modifié alors qu'il ne devait pas l'être.")
        self.assertEqual(self.match_quiz.text, initial_text, "Le texte a été modifié alors qu'il ne devait pas l'être.")
        updated_pairs = list(self.match_quiz.pairs.all())
        self.assertPairsMatch(initial_pairs, updated_pairs)

    # 403 Permission
    @skip("TODO")
    def test_update_match_quiz_different_user(self):
        """Test pour vérifier qu'un utilisateur non propriétaire ne peut pas mettre à jour un quiz."""
        self.client.force_authenticate(self.other_user)

        updated_data = {
            "title": "Unauthorized Update Title",
            "text": "Unauthorized Update Description",
            "pairs": [{"text_clue": "France", "answer": "Paris"}]
        }
        response = self.client.put(
            self.match_quiz_update_url,
            updated_data,
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class TestMatchQuizPartialUpdateEndpoint(TestMatchQuiz):

    # 401
    def test_partial_update_match_quiz_unauthenticated(self):
        """Test pour vérifier qu'une mise à jour partielle échoue sans authentification."""
        updated_data = {
            "title": "Unauthorized Partial Update Title"
        }
        response = self.client.patch(
            self.match_quiz_update_url,
            updated_data,
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # 200
    def test_partial_update_match_quiz(self):
        """Test pour vérifier qu'une mise à jour partielle fonctionne avec une authentification valide."""
        self.client.force_authenticate(self.user)
        updated_data = {
            "title": "Partially Updated Title",
            "pairs": [{"text_clue": "Allemagne", "answer": "Berlin"}]
        }
        response = self.client.patch(
            self.match_quiz_update_url,
            updated_data,
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.match_quiz.refresh_from_db()
        self.assertEqual(self.match_quiz.title, updated_data["title"])
        self.assertEqual(self.match_quiz.text, "Initial Quiz Description")
        self.assertTrue(self.match_quiz.valid)

    @skip("TODO")
    def test_update_match_quiz_partial_fields(self):
        """Vérifier qu'une mise à jour partielle ne modifie pas les champs non envoyés."""
        self.client.force_authenticate(self.user)
        initial_count = self.match_quiz.pairs.count()
        updated_data = {"title": "Titre mis à jour"}
        response = self.client.patch(
            self.match_quiz_update_url,
            updated_data,
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.match_quiz.refresh_from_db()
        self.assertEqual(self.match_quiz.title, updated_data["title"])
        self.assertEqual(self.match_quiz.text, "Initial Quiz Description")
        self.assertEqual(self.match_quiz.valid, True)
        self.assertEqual(self.match_quiz.pairs.count(), initial_count)

    # 403
    @skip("TODO")
    def test_partial_update_match_quiz_different_user(self):
        """Test pour vérifier qu'un utilisateur non propriétaire ne peut pas effectuer une mise à jour partielle."""
        self.client.force_authenticate(self.other_user)
        updated_data = {
            "title": "Unauthorized Partial Update Title",
            "pairs": [{"text_clue": "France", "answer": "Paris"}]
        }
        response = self.client.patch(
            self.match_quiz_update_url,
            updated_data,
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
