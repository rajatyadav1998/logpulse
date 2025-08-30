import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base  # ✅ updated import

# ✅ Read database URL from environment variable (for pytest & Docker)
SQLALCHEMY_DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:postgres@localhost:5432/logpulsedb"  # fallback for local
)

# ✅ Create engine & session
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# ✅ Base model class (SQLAlchemy 2.0+)
Base = declarative_base()
