# 🚀 Task Manager API

Une API REST complète pour gérer des tâches, construite avec **FastAPI** et **SQLAlchemy**.

![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![Python](https://img.shields.io/badge/python-3.10+-blue.svg)
![Tests](https://img.shields.io/badge/tests-passing-brightgreen)

## ✨ Fonctionnalités

- ✅ CRUD complet (Create, Read, Update, Delete)
- ✅ Validation automatique des données avec Pydantic
- ✅ Documentation interactive (Swagger UI)
- ✅ Tests unitaires avec pytest
- ✅ Base de données SQLite (dev) / PostgreSQL (prod)

## 🛠️ Technologies

- **FastAPI** - Framework web moderne et rapide
- **SQLAlchemy** - ORM Python
- **Pydantic** - Validation de données
- **pytest** - Tests unitaires
- **Uvicorn** - Serveur ASGI

## 📦 Installation
```bash
# Cloner le repo
git clone https://github.com/USERNAME/task-api.git
cd task-api

# Créer un environnement virtuel
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows

# Installer les dépendances
pip install -r requirements.txt
```

## 🚀 Utilisation
```bash
# Lancer le serveur
uvicorn app.main:app --reload

# L'API sera accessible sur http://127.0.0.1:8000
# Documentation : http://127.0.0.1:8000/docs
```

## 🧪 Tests
```bash
# Lancer les tests
pytest

# Avec couverture
pytest --cov=app tests/
```

## 📚 Endpoints

| Méthode | Endpoint | Description |
|---------|----------|-------------|
| GET | `/` | Page d'accueil |
| POST | `/tasks/` | Créer une tâche |
| GET | `/tasks/` | Lire toutes les tâches |
| GET | `/tasks/{id}` | Lire une tâche |
| PUT | `/tasks/{id}` | Modifier une tâche |
| DELETE | `/tasks/{id}` | Supprimer une tâche |

## 📖 Exemple d'Utilisation
```python
import requests

# Créer une tâche
response = requests.post('http://127.0.0.1:8000/tasks/', json={
    'title': 'Apprendre FastAPI',
    'description': 'Faire le mini-projet',
    'completed': False
})

print(response.json())
# {'id': 1, 'title': 'Apprendre FastAPI', ...}
```

## 🔜 Améliorations Futures

- [ ] Authentification JWT
- [ ] Filtrage et pagination
- [ ] Webhooks
- [ ] Déploiement sur cloud (Heroku/Render)

## 📝 Licence

MIT

## 👤 Auteur

**Ton Nom**
- GitHub: [@OwenOuoba](https://github.com/USERNAME)
- LinkedIn: [Thiabrimani Ouoba](https://www.linkedin.com/in/thiabrimani-ouoba-a53364361/)