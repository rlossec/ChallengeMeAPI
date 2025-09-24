


from rest_framework import status
from rest_framework.reverse import reverse

from ...models import Theme
from ...tests.test_themes import TestThemes, NOT_FOUND_ID


class ReorderSubthemesTestCase(TestThemes):

    # -- POST /api/themes/<theme_id>/reorder_subthemes/ -- #
    def test_reorder_subthemes_success(self):
        url = reverse('theme-reorder-subthemes', args=[self.parent_theme.id])
        payload = {"subtheme_order": [self.subtheme3.id, self.subtheme1.id, self.subtheme2.id]}

        self.client.force_authenticate(self.user)

        response = self.client.post(url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], "L'ordre des sous-thèmes a été mis à jour avec succès.")

        # Vérifie que l'ordre a bien été mis à jour
        self.subtheme1.refresh_from_db()
        self.subtheme2.refresh_from_db()
        self.subtheme3.refresh_from_db()

        self.assertEqual(self.subtheme1.order, 1)
        self.assertEqual(self.subtheme2.order, 2)
        self.assertEqual(self.subtheme3.order, 0)

    def test_reorder_subthemes_invalid_subtheme(self):
        url = reverse('theme-reorder-subthemes', args=[self.parent_theme.id])
        payload = {"subtheme_order": [NOT_FOUND_ID, self.subtheme1.id]}

        self.client.force_authenticate(self.user)
        response = self.client.post(url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Certains sous-thèmes ne correspondent pas", response.data['error'])

    def test_reorder_subthemes_with_subtheme_not_in_parent(self):
        other_theme = Theme.objects.create(name="Other Theme")
        url = f"/api/themes/{self.parent_theme.id}/reorder_subthemes/"
        payload = {"subtheme_order": [self.subtheme1.id, other_theme.id]}  # other_theme est invalide

        self.client.force_authenticate(self.user)

        response = self.client.post(url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Certains sous-thèmes ne correspondent pas", response.data['error'])

    def test_reorder_subthemes_empty_list(self):
        url = reverse('theme-reorder-subthemes', args=[self.parent_theme.id])
        payload = {"subtheme_order": []}

        self.client.force_authenticate(self.user)

        response = self.client.post(url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('This list may not be empty.', response.data['subtheme_order'])

    def test_reorder_subthemes_invalid_data_type(self):
        url = reverse('theme-reorder-subthemes', args=[self.parent_theme.id])
        payload = {"subtheme_order": "not_a_list"}  # Mauvais type de données

        self.client.force_authenticate(self.user)

        response = self.client.post(url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Expected a list of items but got type "str".', response.data['subtheme_order'])
