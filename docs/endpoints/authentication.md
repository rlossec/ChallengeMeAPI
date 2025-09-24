# Synthèse

|  | url | Description | Implement | Tests | Shortcut |
| --- | --- | --- | --- | --- | --- |
| **POST**	 | `auth/users/` | Register | 15 ✅ | ✅ | [Détail](#1-inscription) |
| --- | --- | --- | --- | --- | --- |
| **POST** | `auth/users/activation/` | Activate account | ❌ | ❌ | [Détail](#21-activation) |
| **POST**	 | `auth/users/resend_activation/` | Resend activation email | ❌ | ❌ | [Détail](#22-renvoi-de-lemail-dactivation) |
| --- | --- | --- | --- | --- | --- |
| **POST** | `auth/jwt/create/` | Login -> JWT Tokens | ❌ | ❌ | [Détail](#3-connexion) |
| --- | --- | --- | --- | --- | --- |
| **POST** | `auth/jwt/refresh/` | Refresh JWT Token | ❌ | ❌ | [Détail](#41-rafraîchissement-du-token) |
| **POST** | `auth/jwt/verify/` | Delete | ❌| ❌ | [Détail](#42-vérification-du-token) |
| --- | --- | --- | --- | --- | --- |
| **GET**	 | `auth/users/` | List users | ❌ | ❌ | [Détail](#5-liste-les-utilisateurs) |
| --- | --- | --- | --- | --- | --- |
| **GET**	 | `auth/users/me/` | Detail | ❌ | ❌ | [Détail](#61-récupération) |
| **PUT** | `auth/users/me/` | Update | ❌ | ❌ | [Détail](#62-mise-à-jour)  |
| **PATCH** | `auth/users/me/` | Partial Update | ❌ | ❌ | [Détail](#63-mise-à-jour-partielle)  |
| **DELETE** | `auth/users/me/` | Delete | ❌| ❌ | [Détail](#64-suppression) |
| --- | --- | --- | --- | --- | --- |
| **GET**	 | `auth/users/<user_id>/` | Detail | ❌ | ❌ | [Détail](#71-récupération)  |
| **PUT** | `auth/users/<user_id>/` | Update | ❌ | ❌ | [Détail](#72-mise-à-jour)  |
| **PATCH** | `auth/users/<user_id>/` | Partial Update | ❌ | ❌ | [Détail](#73-mise-à-jour-partielle)  |
| **DELETE** | `auth/users/<user_id>/` | Delete | ❌| ❌ | [Détail](#74-suppression) |
| --- | --- | --- | --- | --- | --- |
| **POST**	 | `auth/users/reset_password/` | Reset pwd | ❌ | ❌ | [Détail](#81-requête-mot-de-passe) |
| **POST** | `auth/users/reset_password_confirm/` | Confirm pwd reset | ❌ | ❌ | [Détail](#82-confirmation-mot-de-passe) |
| **POST** | `auth/users/reset_username/` | Reset username | ❌ | ❌ | [Détail](#83-requête-nom-dutilisateur) |
| **POST** | `auth/users/reset_username_confirm/` | Confirm username reset | ❌| ❌ | [Détail](#84-confirmation-nom-dutilisateur) |
| --- | --- | --- | --- | --- | --- |
| **POST** | `auth/users/set_password` | Set password | ❌ | ❌ | [Détail](#91-changement-de-mot-de-passe) |
| **POST** | `auth/users/set_username/` | Set username | ❌| ❌ | [Détail](#92-changement-du-nom-dutilisateur) |

✅/❌

---
# Détail


## 1. Inscription

**POST** `auth/users/`

**Description** : Crée un nouvel utilisateur.
**Commande des tests** : `python manage.py test accounts.tests.test_register`

#### Paramètres

```json
{
  "username": "string",
  "email": "string",
  "password": "string",
  "re_password": "string"
}
```

#### Réponse 201

```json
{
  "id": 1,
  "username": "testuser",
  "email": "test@example.com",
}
```

#### Cas d'erreur

- **400** : 
  * Champ obligatoire manquant (username, email, password, re_password) ✅
  * Données invalides :                                                 ✅
    - usename avec des caractères spéciaux                              ✅
    - username trop long                                                ✅
    - username existant en BDD                                          ✅
    - email invalide (ne respectant pas la structure aaa@aa.aaa)        ✅
    - email existant en BDD                                             ✅
    - les deux mots de passes ne match pas                              ✅
    - le mot de passe est trop court                                    ✅
    - le mot de passe est trop commun                                   ✅
    - le mot de passe ne contient que des nombres                       ✅
    - le mot de passe est trop similaire au username                    ✅

## 2. Activation de compte

**Commande des tests** : `python manage.py test accounts.tests.test_activation`

### 2.1. Activation

**POST** `auth/users/activation/`

**Description** : Active un compte utilisateur.

#### Paramètres

```json
{
  "uid": "string",
  "token": "string"
}
```

### 2.2. Renvoi de l'email d'activation

**POST** `auth/resend_activation/`

**Description** : Renvoi le mail pour activer son compte
**Commande des tests** : `python manage.py test accounts.tests.test_activation`

#### Paramètres

```json
{
  "uid": "string",
  "token": "string"
}
```

## 3. Connexion

**POST** `/auth/jwt/create/`

**Description** : Authentifie un utilisateur et retourne les tokens JWT.
**Commande des tests** : `python manage.py test accounts.tests.test_jwt`


#### Paramètres

```json
{
  "username": "string",
  "password": "string"
}
```

#### Réponse de succès (200)

```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

#### Codes d'erreur

- **401** : Identifiants invalides

## 4. Gestion des JWT
### 4.1 Rafraîchissement du token

**POST** `/auth/jwt/refresh/`

**Description** : Renouvelle le token d'accès.
**Commande des tests** : `python manage.py test accounts.tests.test_jwt`


#### Paramètres

```json
{
  "refresh": "string"
}
```

#### Réponse de succès (200)

```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

### 4.2. Vérification du token

**POST** `/auth/jwt/verify/`

**Description** : Vérifie la validité d'un JWT.
**Commande des tests** : `python manage.py test accounts.tests.test_jwt`

## 5. Liste les utilisateurs

**GET** `/auth/users/`

**Description** : Liste les utilisateurs actifs
**Commande des tests** : `python manage.py test accounts.tests.` xxxx



## 6. Son profil utilisateur

### 6.1. Récupération
**GET** `/auth/users/me/`

**Description** : Récupère le profil de l'utilisateur connecté (lié au JWT)
**Commande des tests** : `python manage.py test accounts.tests.` xxxx


#### Réponse de succès (200)

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



### 6.2. Mise à jour 

 **PATCH** `/auth/users/me/`

Met à jour le profil de l'utilisateur connecté.


### 6.3. Mise à jour partielle

 **PATCH** `/auth/users/me/`

Met à jour le profil de l'utilisateur connecté.


### 6.4. Suppression 

 **PATCH** `/auth/users/me/`

Supprime le profil de l'utilisateur connecté.

## 7. Profil utilisateur avec son id

### 7.1. Récupération

**GET** `/auth/users/<user_id>/`

**Description** : Récupère le profil de l'utilisateur associé à l'id
**Commande des tests** : `python manage.py test accounts.tests.` xxxx


#### Réponse de succès (200)

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



### 7.2. Mise à jour 

 **PATCH** `/auth/users/<user_id>/`

Met à jour le profil de l'utilisateur.


### 7.3. Mise à jour partielle

 **PATCH** `/auth/users/<user_id>/`

Met à jour le profil de l'utilisateur.


### 7.4. Suppression 

 **PATCH** `/auth/users/<user_id>/`

Supprime le profil de l'utilisateur


## 8. Réinitialisations

### 8.1. Requête mot de passe

**POST** `/auth/users/reset_password/`

Demande une réinitialisation de mot de passe.

#### Paramètres

```json
{
  "email": "string"
}
```

### 8.2. Confirmation mot de passe

**POST** `/auth/users/reset_password_confirm/`

Confirme la réinitialisation avec le token.

#### Paramètres

```json
{
  "uid": "string",
  "token": "string",
  "new_password": "string",
  "re_new_password": "string"
}
```


### 8.3. Requête nom d'utilisateur

### 8.4. Confirmation nom d'utilisateur



## 9. Changement des informations sensibles


### 9.1. Changement de mot de passe

**POST** `/auth/users/set_password/`

Change le mot de passe de l'utilisateur connecté.

#### Paramètres

```json
{
  "current_password": "string",
  "new_password": "string",
  "re_new_password": "string"
}
```

### 9.2. Changement du nom d'utilisateur

**POST** `/auth/users/set_username/`

Change le mot de passe de l'utilisateur connecté.

#### Paramètres

```json
{
  "current_password": "string",
  "new_username": "string",
}
```