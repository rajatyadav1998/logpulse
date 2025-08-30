![Tests](https://github.com/rajatyadav1998/logpulse/actions/workflows/tests.yml/badge.svg)
![Python](https://img.shields.io/badge/python-3.11%2B-blue)
![License](https://img.shields.io/badge/License-MIT-green)

# 🚀 LogPulse


🚀 LogPulse

LogPulse is a backend logging & monitoring system built with FastAPI, PostgreSQL, SQLAlchemy, Alembic, Docker, and JWT Authentication.
It provides secure role-based access (RBAC) where admins can manage logs and users can submit/view logs.

✨ Features

🔐 JWT Authentication – Secure login with token-based authentication

👤 Role-Based Access Control (RBAC) – Users vs Admins

📝 Log Management – Create, view, and search logs

🗑️ Admin Privileges – Delete logs with admin role

🗄️ Database Migrations – Managed with Alembic

🐳 Dockerized Setup – Easy to run using Docker & docker-compose

🧪 Pytest Test Suite – Automated testing for endpoints

📜 Logging – Tracks user creation and login in app.log

🏗️ Tech Stack

Backend Framework: FastAPI

Database: PostgreSQL

ORM: SQLAlchemy

Migrations: Alembic

Authentication: OAuth2 with JWT (JSON Web Tokens)

Testing: Pytest + FastAPI TestClient

Containerization: Docker & Docker Compose

Logging: Python Logging Module (app.log)

⚡ Setup Instructions
1️⃣ Clone Repository
git clone https://github.com/rajatyadav1998/logpulse.git
cd logpulse

2️⃣ Create Virtual Environment & Install Dependencies
py -3.11 -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

3️⃣ Setup Database

Make sure PostgreSQL is running. Update .env with your database details.

Run migrations:

alembic upgrade head

4️⃣ Start the Server
uvicorn main:app --reload


Server will be live at 👉 http://127.0.0.1:8000

🔑 Example API Usage
Register User
curl -X POST "http://127.0.0.1:8000/users/" ^
-H "Content-Type: application/json" ^
-d "{\"email\":\"user1@example.com\", \"password\":\"userpass\", \"role\":\"user\"}"

Login (Get Token)
curl -X POST "http://127.0.0.1:8000/token" ^
-H "Content-Type: application/x-www-form-urlencoded" ^
-d "username=user1@example.com&password=userpass"

Create Log
curl -X POST "http://127.0.0.1:8000/logs/" ^
-H "Authorization: Bearer <TOKEN>" ^
-H "Content-Type: application/json" ^
-d "{\"message\":\"This is a user log\"}"

Search Logs
curl -X GET "http://127.0.0.1:8000/logs/?search=user1" ^
-H "Authorization: Bearer <TOKEN>"

Delete Log (Admin only)
curl -X DELETE "http://127.0.0.1:8000/logs/1" ^
-H "Authorization: Bearer <ADMIN_TOKEN>"

🧪 Running Tests
pytest -v

👤 Author

Rajat Yadav
🔗 GitHub Profile

📧 rajatyadav1998@gmail.com