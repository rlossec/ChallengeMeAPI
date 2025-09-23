# ChallengeMe Backend

Backend Django REST API pour l'application ChallengeMe - une plateforme de quiz et de défis éducatifs.

## 📋 Description

ChallengeMe est une application web permettant de créer et de participer à différents types de quiz éducatifs. Le backend fournit une API REST complète avec authentification JWT, gestion des utilisateurs, et différents types de quiz.

## 🚀 Fonctionnalités

### Authentification & Utilisateurs

- **Inscription/Connexion** avec username, email et mot de passe
- **Authentification JWT** avec tokens d'accès et de rafraîchissement
- **Gestion des profils**
- **Activation de compte** par email

### Types de Quiz

- **Quiz Classique** : Questions à choix multiples ou texte libre
- **Quiz d'Énumération** : Liste d'éléments à énumérer
- **Quiz de Correspondance** : Associer des éléments par paires

### Gestion des Thèmes

- **Thèmes hiérarchiques** avec sous-thèmes
- **Images et couleurs** personnalisées
- **Système de favoris** par utilisateur
- **Ordre personnalisable** des thèmes

## 🛠️ Technologies

- **Django 5.1.4** - Framework web Python
- **Django REST Framework 3.15.2** - API REST
- **Django Simple JWT 5.3.1** - Authentification JWT
- **Djoser 2.3.1** - Authentification
- **Pillow 11.1.0** - Traitement d'images
- **Django CORS Headers 4.6.0** - Gestion CORS


## 📁 Structure du Projet

```
src/
├── accounts/          # Gestion des utilisateurs et authentification
├── quiz/              # Application principale des quiz
├── config/            # Configuration Django
└── media/             # Fichiers média (avatars, images)
```

## 🚀 Installation et Configuration

### Prérequis

- Python 3.8+
- pip

### Installation

1. **Cloner le projet**

```bash
git clone <repository-url>
cd challenge-backend
```

2. **Installer les dépendances**

Créer et activer l'environnement virtuel

```bash
python -m venv venv
source ./venv/scripts/activate
```

```bash
pip install -r requirements.txt
```

3. **Configuration de l'environnement**
   Créer un fichier `.env` à la racine du projet :

```env
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost 127.0.0.1
CORS_ALLOW_CREDENTIALS=True
CORS_ALLOWED_ORIGINS=http://localhost:3000
CORS_ORIGIN_WHITELIST=http://localhost:3000
CSRF_TRUSTED_ORIGINS=http://localhost:3000
```

4. **Migrations de la base de données**

```bash
cd src
python manage.py makemigrations
python manage.py migrate
```

5. **Créer un superutilisateur**

```bash
python manage.py createsuperuser
```

6. **Lancer le serveur de développement**

```bash
python manage.py runserver
```

Le serveur sera accessible sur `http://localhost:8000/`



## 🧪 Tests

Exécuter les tests :

```bash
cd src
python manage.py test
```

Les tests couvrent :

- Authentification et gestion des utilisateurs
- CRUD des thèmes, questions et quiz
- Logique métier des différents types de quiz
- Gestion des favoris

## 📖 Documentation Complète

Consultez le dossier `docs/` pour :

- **[API Reference](./api.md)** - Documentation détaillée de l'API REST
- **[Documentation des Tests](./tests.md)** - Guide complet des tests unitaires et d'intégration


## 🤝 Contribution

1. Fork le projet
2. Créer une branche feature (`git checkout -b feature/AmazingFeature`)
3. Commit les changements (`git commit -m 'Add some AmazingFeature'`)
4. Push vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrir une Pull Request

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

