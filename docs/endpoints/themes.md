
# Synthèse

|  | url | Description | Implement | Tests |
| --- | --- | --- | --- | --- |
| **GET**	 | `themes/` | List | ❌ | ❌ |
| **POST** | `themes/` | Add | ❌ | ❌ |
| **GET**	 | `themes/<theme_id>/` | Detail | ❌ | ❌ |
| **PUT** | `themes/<theme_id>/` | Update | ❌ | ❌ |
| **PATCH** | `themes/<theme_id>/` | Partial Update | ❌ | ❌ |
| **DELETE** | `themes/<theme_id>/` | Delete | ❌| ❌ |


# Cas par cas

## Thèmes

### Liste des thèmes

**GET** `/quiz/themes/`

Récupère la liste de tous les thèmes.

#### Paramètres de requête

- `parent` : ID du thème parent (optionnel)
- `search` : Recherche par nom (optionnel)

#### Réponse de succès (200)

```json
[
  {
    "id": 1,
    "name": "Sciences",
    "description": "Thème scientifique",
    "parent_theme": null,
    "image": "/media/theme_images/science.jpg",
    "color": "#FF5733",
    "order": 1,
    "subthemes": [
      {
        "id": 2,
        "name": "Physique",
        "order": 1
      }
    ]
  }
]
```

### Détail d'un thème

**GET** `/quiz/themes/{id}/`

Récupère les détails d'un thème spécifique.

#### Réponse de succès (200)

```json
{
    "id": 1,
    "name": "Sciences",
    "description": "Thème scientifique",
    "parent_theme": null,
    "image": "/media/theme_images/science.jpg",
    "color": "#FF5733",
    "order": 1,
    "subthemes": [...],
    "questions_count": 25
}
```

### Création d'un thème

**POST** `/quiz/themes/`

Crée un nouveau thème.

#### Paramètres

```json
{
  "name": "string",
  "description": "string",
  "parent_theme": "integer",
  "image": "file",
  "color": "string",
  "order": "integer"
}
```

#### Réponse de succès (201)

```json
{
  "id": 3,
  "name": "Nouveau thème",
  "description": "Description du thème",
  "parent_theme": 1,
  "image": "/media/theme_images/new.jpg",
  "color": "#00FF00",
  "order": 2
}
```

### Mise à jour d'un thème

**PATCH** `/quiz/themes/{id}/`

Met à jour un thème existant.

#### Paramètres

```json
{
  "name": "string",
  "description": "string",
  "order": "integer"
}
```

### Suppression d'un thème

**DELETE** `/quiz/themes/{id}/`

Supprime un thème.

#### Réponse de succès (204)

Pas de contenu retourné.

## Favoris

### Liste des favoris

**GET** `/quiz/favorites/`

Récupère les thèmes favoris de l'utilisateur connecté.

#### Réponse de succès (200)

```json
[
  {
    "id": 1,
    "user": 1,
    "theme": {
      "id": 1,
      "name": "Sciences",
      "description": "Thème scientifique",
      "color": "#FF5733",
      "image": "/media/theme_images/science.jpg"
    },
    "added_at": "2024-01-01T00:00:00Z"
  }
]
```

### Ajouter un favori

**POST** `/quiz/favorites/add/{theme_id}/`

Ajoute un thème aux favoris.

#### Réponse de succès (201)

```json
{
  "detail": "Theme added to favorites."
}
```

#### Codes d'erreur

- **400** : Thème déjà dans les favoris
- **404** : Thème introuvable

### Supprimer un favori

**DELETE** `/quiz/favorites/remove/{theme_id}/`

Retire un thème des favoris.

#### Réponse de succès (200)

```json
{
  "detail": "Theme removed from favorites."
}
```

#### Codes d'erreur

- **404** : Favori introuvable
