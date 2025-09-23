# Synthèse

|  | url | Description | Implement | Tests |
| --- | --- | --- | --- | --- |
| **GET**	 | `quiz/` | List | ❌ | ❌ |
| **POST** | `quiz/` | Add | ❌ | ❌ |
| --- | --- | --- | --- | --- |
| **GET**	 | `quiz/classic/` | List | ❌ | ❌ |
| **POST** | `quiz/classic/` | Add | ❌ | ❌ |
| **PUT** | `questions/<question_id>/` | Update | ❌ | ❌ |
| **PATCH** | `questions/<question_id>/` | Partial Update | ❌ | ❌ |
| **DELETE** | `questions/<question_id>/` | Delete | ❌| ❌ |
| --- | --- | --- | --- | --- |
| **GET**	 | `quiz/match/` | List | ❌ | ❌ |
| **POST** | `quiz/match/` | Add | ❌ | ❌ |
| **PUT** | `questions/<question_id>/` | Update | ❌ | ❌ |
| **PATCH** | `questions/<question_id>/` | Partial Update | ❌ | ❌ |
| **DELETE** | `questions/<question_id>/` | Delete | ❌| ❌ |
| --- | --- | --- | --- | --- |
| **GET**	 | `quiz/enum/` | List | ❌ | ❌ |
| **POST** | `quiz/enum/` | Add | ❌ | ❌ |
| **PUT** | `questions/<question_id>/` | Update | ❌ | ❌ |
| **PATCH** | `questions/<question_id>/` | Partial Update | ❌ | ❌ |
| **DELETE** | `questions/<question_id>/` | Delete | ❌| ❌ |

✅/❌

# Cas par cas


## Quiz Classiques

### Liste des quiz classiques

**GET** `/quiz/classic-quiz/`

Récupère la liste des quiz classiques.

#### Paramètres de requête

- `creator` : ID du créateur (optionnel)
- `themes` : IDs des thèmes séparés par des virgules
- `valid_only` : true/false (optionnel)

#### Réponse de succès (200)

```json
[
  {
    "id": "uuid",
    "type": "CL",
    "title": "Quiz de Géographie",
    "creator": 1,
    "creator_username": "testuser",
    "themes": [1, 2],
    "themes_names": ["Sciences", "Géographie"],
    "difficulty": 2.5,
    "valid": true,
    "questions_count": 10,
    "created_at": "2024-01-01T00:00:00Z",
    "updated_at": "2024-01-01T00:00:00Z"
  }
]
```

### Détail d'un quiz classique

**GET** `/quiz/classic-quiz/{id}/`

Récupère les détails d'un quiz classique avec ses questions.

### Création d'un quiz classique

**POST** `/quiz/classic-quiz/`

Crée un nouveau quiz classique.

#### Paramètres

```json
{
  "title": "string",
  "themes": ["integer"],
  "questions": ["integer"],
  "difficulty": "float"
}
```

## Quiz d'Énumération

### Liste des quiz d'énumération

**GET** `/quiz/enum-quiz/`

Récupère la liste des quiz d'énumération.

### Détail d'un quiz d'énumération

**GET** `/quiz/enum-quiz/{id}/`

Récupère les détails d'un quiz d'énumération avec ses réponses.

### Création d'un quiz d'énumération

**POST** `/quiz/enum-quiz/`

Crée un nouveau quiz d'énumération.

#### Paramètres

```json
{
  "title": "string",
  "text": "string",
  "themes": ["integer"],
  "enum_answers": [
    {
      "answer_text_fr": "string",
      "answer_text_en": "string",
      "order": "integer"
    }
  ]
}
```

## Quiz de Correspondance

### Liste des quiz de correspondance

**GET** `/quiz/match-quiz/`

Récupère la liste des quiz de correspondance.

### Détail d'un quiz de correspondance

**GET** `/quiz/match-quiz/{id}/`

Récupère les détails d'un quiz de correspondance avec ses paires.

### Création d'un quiz de correspondance

**POST** `/quiz/match-quiz/`

Crée un nouveau quiz de correspondance.

#### Paramètres

```json
{
  "title": "string",
  "text": "string",
  "themes": ["integer"],
  "base_url": "string",
  "pairs": [
    {
      "text_clue": "string",
      "picture_clue": "string",
      "answer": "string"
    }
  ]
}
```


## Quiz
### Créer un quiz Random ❌

**Endpoint : `POST /quiz/create/`**
