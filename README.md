# 🚀 LogPulse

**LogPulse** is a backend logging & monitoring system built with **FastAPI, PostgreSQL, SQLAlchemy, Alembic, Docker, and JWT Authentication**.  
It provides secure role-based access (RBAC) where **admins** can manage logs and users can submit/view logs.

---
## ✨ Features

- 🔐 **JWT Authentication** – Secure login with token-based authentication  
- 👤 **Role-Based Access Control (RBAC)** – Users vs Admins  
- 📝 **Log Management** – Create, view, and search logs  
- 🗑️ **Admin Privileges** – Delete logs with admin role  
- 🗄️ **Database Migrations** – Managed with Alembic  
- 🐳 **Dockerized Setup** – Easy to run using Docker & docker-compose  
- 🧪 **Pytest Test Suite** – Automated testing for endpoints  
- 📜 **Logging** – Tracks user creation and login in `app.log`
## 🏗️ Tech Stack

- **Backend Framework**: FastAPI  
- **Database**: PostgreSQL  
- **ORM**: SQLAlchemy  
- **Migrations**: Alembic  
- **Authentication**: OAuth2 with JWT (JSON Web Tokens)  
- **Testing**: Pytest + FastAPI TestClient  
- **Containerization**: Docker & Docker Compose  
- **Logging**: Python Logging Module (`app.log`)  

## ⚡ Setup Instructions

Follow these steps to run the project locally:

### 1️⃣ Clone Repository
```bash
git clone https://github.com/rajatyadav1998/logpulse.git
cd logpulse

### 2️⃣ Create Virtual Environment & Install Dependencies
```bash
python -m venv venv
venv\Scripts\activate   # On Windows
source venv/bin/activate   # On Linux/Mac

pip install -r requirements.txt
