import sys, os

# ✅ Add project root to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base
from main import app, get_db   # ✅ import correctly

# ✅ Use Docker Postgres (change if needed)
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/logpulsedb"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# ✅ Reset DB for tests
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

# ✅ Override dependency
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

# --- Helpers ---
def create_user(email: str, password: str, role: str) -> dict[str, str]:
    response = client.post(
        "/users/",
        json={"email": email, "password": password, "role": role}
    )
    assert response.status_code in [200, 400]
    return response.json()

def get_token(email: str, password: str) -> str:
    response = client.post(
        "/token",
        data={"username": email, "password": password},
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    assert response.status_code == 200
    data: dict[str, str] = response.json()
    return data["access_token"]

# --- Tests ---
def test_create_user():
    user = create_user("pytestuser@example.com", "pytestpass", "user")
    assert "email" in user

def test_create_admin():
    admin = create_user("pytestadmin@example.com", "pytestpass", "admin")
    assert "email" in admin

def test_login_and_create_log():
    token = get_token("pytestuser@example.com", "pytestpass")
    response = client.post(
        "/logs/",
        json={"message": "pytest log entry"},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data: dict[str, str] = response.json()
    assert data["message"] == "pytest log entry"

def test_filter_logs():
    token = get_token("pytestuser@example.com", "pytestpass")
    response = client.get(
        "/logs/?search=pytest",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data: list[dict[str, str]] = response.json()
    assert any("pytest" in log["message"] for log in data)

def test_admin_delete_log():
    admin_token = get_token("pytestadmin@example.com", "pytestpass")
    response = client.delete(
        "/logs/1",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code in [200, 404]
