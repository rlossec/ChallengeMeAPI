
# Vue d'ensemble

Pour chaque services, on retrouve un fichier avec le détail des endpoints :
- **[Authentification](./authentication.md)**
- **[Questions](./questions.md)**
- **[Thèmes](./themes.md)**
- **[Quiz](./quiz.md)**


# 🔐 Authentification

L'API utilise l'authentification JWT avec des tokens d'accès et de rafraîchissement.

Headers requis

```
Authorization: Bearer <access_token>
Content-Type: application/json
```

# 🔧 Configuration et Déploiement

## Variables d'environnement

```env
SECRET_KEY=your-secret-key
DEBUG=False
ALLOWED_HOSTS=yourdomain.com
CORS_ALLOWED_ORIGINS=https://yourdomain.com
```

## Configuration CORS

```python
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "https://yourdomain.com",
]
CORS_ALLOW_CREDENTIALS = True
```


# 📊 Codes d'Erreur

TODO

# 🔍 Filtrage et Recherche ❌

TODO 

### Paramètres de filtrage communs 

#### Pagination ❌

- `page` : Numéro de page (défaut: 1)
- `page_size` : Taille de page (défaut: 20, max: 100)

#### Tri ❌

- `ordering` : Champ de tri (préfixe `-` pour ordre décroissant)
- Exemples : `ordering=created_at`, `ordering=-difficulty`

#### Recherche ❌

- `search` : Recherche textuelle dans les champs pertinents

### Exemples d'utilisation

#### Questions filtrées par thème et difficulté

```
GET /quiz/questions/?theme=1&difficulty_min=1&difficulty_max=3&ordering=-created_at
```

#### Quiz classiques d'un créateur

```
GET /quiz/classic-quiz/?creator=1&valid_only=true&page=1&page_size=10
```

#### Recherche de thèmes

```
GET /quiz/themes/?search=science&ordering=name
```

## 📁 Upload de Fichiers ❌

### Types de fichiers supportés

#### Images

- **Formats** : JPG, PNG, GIF, WebP
- **Taille maximale** : 5MB
- **Dimensions** : Recommandé 800x600px

#### Endpoints d'upload

- **Avatars** : `/media/avatars/`
- **Images de thèmes** : `/media/theme_images/`
- **Images de questions** : `/media/question_images/`


## 🔄 Rate Limiting ❌



### Configuration de production ❌

- **Base de données** : PostgreSQL recommandé
- **Cache** : Redis pour les sessions et le cache
- **Serveur web** : Nginx + Gunicorn
- **HTTPS** : Certificat SSL requis
