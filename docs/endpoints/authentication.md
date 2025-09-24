# Synthèse

|  | url | Description | Implement | Tests | Shortcut |
| --- | --- | --- | --- | --- | --- |
| **POST**	 | `auth/users/` | Register | ✅ | 15 ✅ | [Détail](#1-inscription) |
| --- | --- | --- | --- | --- | --- |
| **POST** | `auth/users/activation/` | Activate account | ✅ | ✅ | [Détail](#21-activation) |
| **POST**	 | `auth/users/resend_activation/` | Resend activation email | ✅ | ✅ | [Détail](#22-renvoi-de-lemail-dactivation) |
| --- | --- | --- | --- | --- | --- |
| **POST** | `auth/jwt/create/` | Login -> JWT Tokens | ✅ | ✅ | [Détail](#3-connexion) |
| --- | --- | --- | --- | --- | --- |
| **POST** | `auth/jwt/refresh/` | Refresh JWT Token | ✅ | ✅ | [Détail](#41-rafraîchissement-du-token) |
| **POST** | `auth/jwt/verify/` | Delete | ✅| ✅ | [Détail](#42-vérification-du-token) |
| --- | --- | --- | --- | --- | --- |
| **GET**	 | `auth/users/` | List users | ✅ | ✅ | [Détail](#5-liste-les-utilisateurs) |
| --- | --- | --- | --- | --- | --- |
| **GET**	 | `auth/users/me/` | Detail | ✅ | ✅ | [Détail](#61-récupération) |
| **PUT** | `auth/users/me/` | Update | ✅ | ✅ | [Détail](#62-mise-à-jour)  |
| **PATCH** | `auth/users/me/` | Partial Update | ✅ | ✅ | [Détail](#63-mise-à-jour-partielle)  |
| **DELETE** | `auth/users/me/` | Delete | ✅| ✅ | [Détail](#64-suppression) |
| --- | --- | --- | --- | --- | --- |
| **GET**	 | `auth/users/<user_id>/` | Detail | ✅ | ✅ | [Détail](#71-récupération)  |
| **PUT** | `auth/users/<user_id>/` | Update | ✅ | ✅ | [Détail](#72-mise-à-jour)  |
| **PATCH** | `auth/users/<user_id>/` | Partial Update | ✅ | ✅ | [Détail](#73-mise-à-jour-partielle)  |
| **DELETE** | `auth/users/<user_id>/` | Delete | ✅| ✅ | [Détail](#74-suppression) |
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
    - username avec des caractères spéciaux                             ✅
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
#### Réponse 204 No Content ❌

#### Cas d'erreur

- **400** : 
  * Champ obligatoire manquant uid ou token ✅
  * Champ invalide uid ou token ✅
- **403** : 
  * Compte déjà actif ✅

### 2.2. Renvoi de l'email d'activation

**POST** `auth/resend_activation/`

**Description** : Renvoi le mail pour activer son compte
**Commande des tests** : `python manage.py test accounts.tests.test_activation`

#### Paramètres

```json
{
  "email": "string",
}
```

#### Réponse 204 NO CONTENT ✅

Pour ne pas communiquer le fait qu'un email est en base de données, on a deux messages de succès fictif :

- Si l'email n'est pas en BDD
- Si l'email correspond à un compte déjà actif

#### Cas d'erreur

- **400** : 
  * Champ obligatoire manquant email ✅
  * Champ invalide email ✅
- **403** : 
  * Compte déjà actif ✅


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

#### Réponse de succès (200) ✅

```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

#### Cas d'erreur

- **401** : 
  * Identifiants invalides ✅
  * Utilisateur inactif ✅
- **400** :
  * Champ obligatoire manquant : username ou password ✅ ✅


Les deux cas 401 renvoi un message indiquant des identifiants invalides pour cacher le fait qu'un email est en BDD.


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

#### Réponse de succès (200) ✅

```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

#### Cas d'erreur

- **400** : Champ refresh manquant ✅
- **401** : Token invalide         ✅

### 4.2. Vérification du token

**POST** `/auth/jwt/verify/`

**Description** : Vérifie la validité d'un JWT.
**Commande des tests** : `python manage.py test accounts.tests.test_jwt`

#### Paramètres

```json
{
  "token": "string"
}
```

#### Réponse de succès (200) ✅

```json
{

}
```
TODO : Override pour soit un 204, soit un booléen true ?


#### Cas d'erreur

- **400** : Champ `token` manquant ✅
- **401** : Token invalide         ✅

## 5. Liste les utilisateurs

**GET** `/auth/users/`  
Privé : Nécessite un JWT  
**Description** : Liste les utilisateurs actifs  
**Commande des tests** : `python manage.py test accounts.tests.test_user_list`

#### Permissions
Un utilisateur simple ne voit que son instance user dans la liste. ✅
Un staff ou superadmin peut voir tous les utilisateurs. ✅ ✅

#### Cas d'erreur

- **401** : Absence de JWT         ✅


## 6. Son profil utilisateur

### 6.1. Récupération

**GET** `/auth/users/me/`  
Privé : Nécessite un JWT  
**Description** : Récupère le profil de l'utilisateur connecté (lié au JWT)  
**Commande des tests** : `python manage.py test accounts.tests.test_user_me`


#### Réponse de succès (200)

```json
{
  "id": 1,
  "username": "testuser",
  "email": "test@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "avatar": "/media/avatars/profile.jpg",
}
```

#### Cas d'erreur

- **401** : Absence de JWT         ✅


### 6.2. Mise à jour 

**PUT** `/auth/users/me/`  
Privé : Nécessite un JWT  
**Description** : Met à jour le profil de l'utilisateur connecté. (lié au JWT)  
**Commande des tests** : `python manage.py test accounts.tests.test_user_me`

#### Body
```json
{
  "email": "test@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "avatar": "/media/avatars/profile.jpg",
}
```

⚠️ Attention:
- L'email est obligatoire, il sert de vérification
- Le changement d'email, mène à la désactivation du compte
- Le username ne peut être modifier ainsi
- Un champ `avatar` vide conduit à la suppression du précédent


#### Cas d'erreur

- **401** : Absence de JWT                          ✅
- **400** : 
  * Champ manquant obligatoire : `email`            ✅
  * `email` invalide                                ✅
  * `email` déjà en BDD                             ✅
  * `first_name` ou `last_name` trop long           ✅



### 6.3. Mise à jour partielle

**PATCH** `/auth/users/me/`
**Description** : Met à jour le profil de l'utilisateur connecté. (lié au JWT)  
**Commande des tests** : `python manage.py test accounts.tests.test_user_me`

#### Body
```json
{
  "email": "test@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "avatar": "/media/avatars/profile.jpg",
}
```

⚠️ Attention:
- Le changement d'email, mène à la désactivation du compte
- Le username ne peut être modifier ainsi
- Un champ `avatar` vide conduit à la suppression du précédent


#### Cas d'erreur

- **401** : Absence de JWT                          ✅
- **400** : 
  * Champ manquant obligatoire : `email`            ✅
  * `email` invalide                                ✅
  * `email` déjà en BDD                             ✅
  * `first_name` ou `last_name` trop long           ✅

### 6.4. Suppression 

**PATCH** `/auth/users/me/`  
Privé : Nécessite un JWT  
**Description** : Supprime le profil de l'utilisateur connecté. (lié au JWT)  
**Commande des tests** : `python manage.py test accounts.tests.test_user_me`

#### Body
```json
{
  "current_password": "******",
}
```
Si le compte est déjà supprimé
```json
{
    "detail": "User not found",
    "code": "user_not_found"
}
```
#### Réponse 204 No content

#### Cas d'erreur

- **401** : 
  * Absence de JWT                                  ✅
  * Compte associé au JWT déjà supprimé             ✅
- **400** : 
  * Champ manquant obligatoire : `current_password` ✅

## 7. Profil utilisateur avec son id

### 7.1. Récupération

**GET** `auth/users/<user_id>/`  
Privé : Nécessite un JWT  

**Description** : Récupère le profil de l'utilisateur associé à l'id
**Commande des tests** : `python manage.py test accounts.tests.test_user_detail`

#### Réponse de succès (200)

```json
{
  "id": 1,
  "username": "testuser",
  "email": "test@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "avatar": "/media/avatars/profile.jpg",

}
```



### 7.2. Mise à jour 

**PATCH** `/auth/users/<user_id>/`  
Privé : Nécessite un JWT  
**Description** : Met à jour le profil de l'utilisateur.
**Commande des tests** : `python manage.py test accounts.tests.test_user_detail`

#### Body
```json
{
  "email": "test@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "avatar": "/media/avatars/profile.jpg",
}
```

⚠️ Attention:
- L'email est obligatoire, il sert de vérification
- Le changement d'email, mène à la désactivation du compte
- Le username ne peut être modifier ainsi
- Un champ `avatar` vide conduit à la suppression du précédent

#### Cas d'erreur

- **401** : Absence de JWT                          ✅
- **400** : 
  * Champ manquant obligatoire : `email`            
  * `email` invalide                                
  * `email` déjà en BDD                             
  * `first_name` ou `last_name` trop long           
- **404** : Id Not Found                            ✅

### 7.3. Mise à jour partielle

**PATCH** `/auth/users/<user_id>/`  
Privé : Nécessite un JWT  
**Description** : Met à jour le profil de l'utilisateur.
**Commande des tests** : `python manage.py test accounts.tests.test_user_detail`

#### Body
```json
{
  "email": "test@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "avatar": "/media/avatars/profile.jpg",
}
```

⚠️ Attention:
- Le changement d'email, mène à la désactivation du compte
- Le username ne peut être modifier ainsi
- Un champ `avatar` vide conduit à la suppression du précédent

#### Cas d'erreur

- **401** : Absence de JWT                          
- **400** :         
  * `email` invalide                                
  * `email` déjà en BDD                             
  * `first_name` ou `last_name` trop long           
- **404** : Id Not Found                            


### 7.4. Suppression 

**PATCH** `/auth/users/<user_id>/`  
Privé : Nécessite un JWT  
**Description** : Supprime le profil de l'utilisateur
**Commande des tests** : `python manage.py test accounts.tests.test_user_detail`

#### Cas d'erreur

- **401** : Absence de JWT                 ✅                        
- **404** : Id Not Found                   ✅

## 8. Réinitialisations

### 8.1. Requête mot de passe

**POST** `/auth/users/reset_password/`  
Public

Demande une réinitialisation de mot de passe.

#### Paramètres

```json
{
  "email": "string"
}
```

### 8.2. Confirmation mot de passe

**POST** `/auth/users/reset_password_confirm/`  
Public  

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

**POST** `auth/users/reset_username/`
Public

### 8.4. Confirmation nom d'utilisateur

**POST** | `auth/users/reset_username_confirm/`
Public


## 9. Changement des informations sensibles


### 9.1. Changement de mot de passe

**POST** `/auth/users/set_password/`
Privé : Nécessite un JWT  
**Description** : Change le mot de passe de l'utilisateur connecté.

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
Privé : Nécessite un JWT  
**Description** : Change le mot de passe de l'utilisateur connecté.

#### Paramètres

```json
{
  "current_password": "string",
  "new_username": "string",
}
```