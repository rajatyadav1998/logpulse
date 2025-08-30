from sqlalchemy.orm import Session
import models, schemas, security

# --- User CRUD Functions ---
def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = security.get_password_hash(user.password)
    db_user = models.User(
        email=user.email,
        hashed_password=hashed_password,
        role=user.role  # ✅ save role correctly
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# --- Log CRUD Functions ---
def create_log(db: Session, log: schemas.LogCreate):
    db_log = models.Log(message=log.message)
    db.add(db_log)
    db.commit()
    db.refresh(db_log)
    return db_log

# ✅ Updated get_logs with filtering
def get_logs(db: Session, skip: int = 0, limit: int = 100, search: str | None = None):
    query = db.query(models.Log)
    if search:
        query = query.filter(models.Log.message.ilike(f"%{search}%"))  # case-insensitive search
    return query.offset(skip).limit(limit).all()
