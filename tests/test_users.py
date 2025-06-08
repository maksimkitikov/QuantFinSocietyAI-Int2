from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.main import app
from app.core.config import settings
from app.crud.user import create_user, get_user_by_email
from app.schemas.user import UserCreate
from app.core.security import get_password_hash

client = TestClient(app)

def test_create_user(db: Session):
    user_data = {
        "email": "test@example.com",
        "username": "testuser",
        "password": "testpass123"
    }
    response = client.post("/api/v1/users/", json=user_data)
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == user_data["email"]
    assert data["username"] == user_data["username"]
    assert "id" in data

def test_read_users(db: Session):
    response = client.get("/api/v1/users/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

def test_read_user(db: Session):
    # Создаем тестового пользователя
    user_data = {
        "email": "test2@example.com",
        "username": "testuser2",
        "password": "testpass123"
    }
    user = create_user(db, UserCreate(**user_data))
    
    response = client.get(f"/api/v1/users/{user.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == user_data["email"]
    assert data["username"] == user_data["username"]

def test_update_user(db: Session):
    # Создаем тестового пользователя
    user_data = {
        "email": "test3@example.com",
        "username": "testuser3",
        "password": "testpass123"
    }
    user = create_user(db, UserCreate(**user_data))
    
    update_data = {
        "username": "updateduser"
    }
    response = client.patch(f"/api/v1/users/{user.id}", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == update_data["username"]

def test_delete_user(db: Session):
    # Создаем тестового пользователя
    user_data = {
        "email": "test4@example.com",
        "username": "testuser4",
        "password": "testpass123"
    }
    user = create_user(db, UserCreate(**user_data))
    
    response = client.delete(f"/api/v1/users/{user.id}")
    assert response.status_code == 200
    
    # Проверяем, что пользователь удален
    db_user = get_user_by_email(db, email=user_data["email"])
    assert db_user is None 