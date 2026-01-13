from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pytest

from app.main import app
from app.database import Base, get_db
from app import models

# Base de données de test (en mémoire, pas de fichier)
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Fixture : setup/teardown pour chaque test
@pytest.fixture
def test_db():
    # Créer les tables
    Base.metadata.create_all(bind=engine)
    yield
    # Supprimer les tables après le test
    Base.metadata.drop_all(bind=engine)

# Override de la dépendance get_db
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

# ========== TESTS ==========

def test_read_root():
    """Test de la page d'accueil"""
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()

def test_create_task(test_db):
    """Test de création d'une tâche"""
    response = client.post(
        "/tasks/",
        json={"title": "Test Task", "description": "Test Description", "completed": False}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test Task"
    assert data["description"] == "Test Description"
    assert data["completed"] == False
    assert "id" in data
    assert "created_at" in data

def test_create_task_without_title(test_db):
    """Test de création sans titre (doit échouer)"""
    response = client.post(
        "/tasks/",
        json={"description": "No title", "completed": False}
    )
    assert response.status_code == 422  # Validation error

def test_get_tasks(test_db):
    """Test de lecture de toutes les tâches"""
    # Créer 2 tâches
    client.post("/tasks/", json={"title": "Task 1", "completed": False})
    client.post("/tasks/", json={"title": "Task 2", "completed": True})
    
    # Lire toutes les tâches
    response = client.get("/tasks/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["title"] == "Task 1"
    assert data[1]["title"] == "Task 2"

def test_get_task_by_id(test_db):
    """Test de lecture d'une tâche spécifique"""
    # Créer une tâche
    create_response = client.post(
        "/tasks/",
        json={"title": "Specific Task", "completed": False}
    )
    task_id = create_response.json()["id"]
    
    # Lire cette tâche
    response = client.get(f"/tasks/{task_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == task_id
    assert data["title"] == "Specific Task"

def test_get_nonexistent_task(test_db):
    """Test de lecture d'une tâche qui n'existe pas"""
    response = client.get("/tasks/9999")
    assert response.status_code == 404

def test_update_task(test_db):
    """Test de mise à jour d'une tâche"""
    # Créer une tâche
    create_response = client.post(
        "/tasks/",
        json={"title": "Original Title", "completed": False}
    )
    task_id = create_response.json()["id"]
    
    # Modifier la tâche
    update_response = client.put(
        f"/tasks/{task_id}",
        json={"title": "Updated Title", "completed": True}
    )
    assert update_response.status_code == 200
    data = update_response.json()
    assert data["title"] == "Updated Title"
    assert data["completed"] == True

def test_update_nonexistent_task(test_db):
    """Test de mise à jour d'une tâche inexistante"""
    response = client.put(
        "/tasks/9999",
        json={"title": "Won't work"}
    )
    assert response.status_code == 404

def test_delete_task(test_db):
    """Test de suppression d'une tâche"""
    # Créer une tâche
    create_response = client.post(
        "/tasks/",
        json={"title": "To Delete", "completed": False}
    )
    task_id = create_response.json()["id"]
    
    # Supprimer la tâche
    delete_response = client.delete(f"/tasks/{task_id}")
    assert delete_response.status_code == 204
    
    # Vérifier qu'elle n'existe plus
    get_response = client.get(f"/tasks/{task_id}")
    assert get_response.status_code == 404

def test_delete_nonexistent_task(test_db):
    """Test de suppression d'une tâche inexistante"""
    response = client.delete("/tasks/9999")
    assert response.status_code == 404

def test_task_has_created_at(test_db):
    """Test que created_at est automatiquement ajouté"""
    response = client.post(
        "/tasks/",
        json={"title": "Time Test", "completed": False}
    )
    data = response.json()
    assert "created_at" in data
    # Vérifier que c'est une date valide
    from datetime import datetime
    datetime.fromisoformat(data["created_at"].replace('Z', '+00:00'))