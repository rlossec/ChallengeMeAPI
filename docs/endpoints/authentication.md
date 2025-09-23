# Synthèse

|  | url | Description | Implement | Tests |
| --- | --- | --- | --- | --- |
| **POST**	 | `auth/users/` | Register | ❌ | ❌ |

| **POST** | `auth/users/activation//` | Activate account | ❌ | ❌ |
| **POST**	 | `auth/users/resend_activation/` | Resend activation email | ❌ | ❌ |

| **POST** | `auth/jwt/create/` | Login -> JWT Tokens | ❌ | ❌ |

| **POST** | `auth/jwt/refresh/` | Refresh JWT Token | ❌ | ❌ |
| **POST** | `auth/jwt/verify/` | Delete | ❌| ❌ |

| **GET**	 | `auth/users/` | List users | ❌ | ❌ |

| **GET**	 | `auth/users/me/` | Detail | ❌ | ❌ |
| **PUT** | `auth/users/me/` | Update | ❌ | ❌ |
| **PATCH** | `auth/users/me/` | Partial Update | ❌ | ❌ |
| **DELETE** | `auth/users/me/` | Delete | ❌| ❌ |

| **GET**	 | `auth/users/<user_id>/` | Detail | ❌ | ❌ |
| **PUT** | `auth/users/<user_id>/` | Update | ❌ | ❌ |
| **PATCH** | `auth/users/<user_id>/` | Partial Update | ❌ | ❌ |
| **DELETE** | `auth/users/<user_id>/` | Delete | ❌| ❌ |

| **POST**	 | `auth/users/reset_password/` | Reset pwd | ❌ | ❌ |
| **POST** | `auth/users/reset_password_confirm/` | Confirm pwd reset | ❌ | ❌ |

| **POST** | `auth/users/reset_username/` | Reset username | ❌ | ❌ |
| **POST** | `auth/users/reset_username_confirm/` | Confirm username reset | ❌| ❌ |

| **POST** | `auth_users_set_password` | Set username | ❌ | ❌ |
| **POST** | `auth/users/set_username/` | Set username | ❌| ❌ |



---
# Détail


## Inscription

**POST** `/auth/users/`

Crée un nouvel utilisateur.

### Paramètres

```json
{
  "username": "string",
  "email": "string",
  "password": "string",
  "re_password": "string"
}
```

### Réponse de succès (201)

```json
{
  "id": 1,
  "username": "testuser",
  "email": "test@example.com",
  "first_name": "",
  "last_name": "",
  "avatar": null,
  "is_active": false
}
```

### Codes d'erreur

- **400** : Données invalides (username existant, email existant, mot de passe faible)
- **401** : Erreurs de validation

## Connexion

**POST** `/auth/jwt/create/`

Authentifie un utilisateur et retourne les tokens JWT.

### Paramètres

```json
{
  "username": "string",
  "password": "string"
}
```

### Réponse de succès (200)

```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

### Codes d'erreur

- **401** : Identifiants invalides

## Rafraîchissement du token

**POST** `/auth/jwt/refresh/`

Renouvelle le token d'accès.

### Paramètres

```json
{
  "refresh": "string"
}
```

### Réponse de succès (200)

```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

## Profil utilisateur

**GET** `/auth/users/me/`

Récupère le profil de l'utilisateur connecté.

### Réponse de succès (200)

```json
{
  "id": 1,
  "username": "testuser",
  "email": "test@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "avatar": "/media/avatars/profile.jpg",
  "is_active": true,
  "date_joined": "2024-01-01T00:00:00Z"
}
```

## Mise à jour du profil

**PATCH** `/auth/users/me/`

Met à jour le profil de l'utilisateur connecté.

### Paramètres

```json
{
  "first_name": "string",
  "last_name": "string",
  "avatar": "file"
}
```

## Changement de mot de passe

**POST** `/auth/users/set_password/`

Change le mot de passe de l'utilisateur connecté.

### Paramètres

```json
{
  "current_password": "string",
  "new_password": "string",
  "re_new_password": "string"
}
```

## Réinitialisation de mot de passe

**POST** `/auth/users/reset_password/`

Demande une réinitialisation de mot de passe.

### Paramètres

```json
{
  "email": "string"
}
```

**POST** `/auth/users/reset_password_confirm/`

Confirme la réinitialisation avec le token.

### Paramètres

```json
{
  "uid": "string",
  "token": "string",
  "new_password": "string",
  "re_new_password": "string"
}
```

## Activation de compte

**POST** `/auth/users/activation/`

Active un compte utilisateur.

### Paramètres

```json
{
  "uid": "string",
  "token": "string"
}
```