# Synthèse

|  | url | Description | Implement | Tests |
| --- | --- | --- | --- | --- |
| **GET**	 | `questions/` | List | ❌ | ❌ |
| **POST** | `questions/` | Add | ❌ | ❌ |
| **GET**	 | `questions/<question_id>/` | Detail | ❌ | ❌ |
| **PUT** | `questions/<question_id>/` | Update | ❌ | ❌ |
| **PATCH** | `questions/<question_id>/` | Partial Update | ❌ | ❌ |
| **DELETE** | `questions/<question_id>/` | Delete | ❌| ❌ |


# Cas par cas

## Liste des questions

**GET** `questions/`

Récupère la liste des questions.

### Paramètres de requête

- `theme` : ID du thème (optionnel)
- `question_type` : Type de question (TXT, IMG, CHO)
- `valid_only` : true/false (optionnel)
- `difficulty_min` : Difficulté minimale (optionnel)
- `difficulty_max` : Difficulté maximale (optionnel)

### Réponse de succès (200)

```json
[
  {
    "id": 1,
    "theme": 1,
    "theme_name": "Sciences",
    "question_type": "TXT",
    "question_text": "Quelle est la capitale de la France ?",
    "image": null,
    "correct_answer": "Paris",
    "accept_close_answer": true,
    "difficulty": 1.0,
    "valid": true,
    "fake_answer_1": null,
    "fake_answer_2": null,
    "fake_answer_3": null,
    "explanation": "Paris est la capitale de la France.",
    "answer_synonyms": ["Paris"],
    "choices": ["Paris"],
    "created_at": "2024-01-01T00:00:00Z",
    "updated_at": "2024-01-01T00:00:00Z"
  }
]
```

## Détail d'une question

**GET** `questions/{id}/`

Récupère les détails d'une question spécifique.

## Création d'une question

**POST** `questions/`

Crée une nouvelle question.

### Paramètres

```json
{
  "theme": "integer",
  "question_type": "string",
  "question_text": "string",
  "image": "file",
  "correct_answer": "string",
  "accept_close_answer": "boolean",
  "difficulty": "float",
  "fake_answer_1": "string",
  "fake_answer_2": "string",
  "fake_answer_3": "string",
  "explanation": "string"
}
```

#### Réponse de succès (201)

```json
{
  "id": 2,
  "theme": 1,
  "theme_name": "Sciences",
  "question_type": "CHO",
  "question_text": "Quelle est la capitale de l'Espagne ?",
  "image": null,
  "correct_answer": "Madrid",
  "accept_close_answer": false,
  "difficulty": 1.5,
  "valid": false,
  "fake_answer_1": "Barcelone",
  "fake_answer_2": "Séville",
  "fake_answer_3": "Valence",
  "explanation": "Madrid est la capitale de l'Espagne.",
  "answer_synonyms": [],
  "choices": ["Madrid", "Barcelone", "Séville", "Valence"],
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": "2024-01-01T00:00:00Z"
}
```

## Mise à jour d'une question

**PATCH** `/quiz/questions/{id}/`

Met à jour une question existante.

## Suppression d'une question

**DELETE** `/quiz/questions/{id}/`

Supprime une question.
