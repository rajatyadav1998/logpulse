import logging
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from jose import JWTError, jwt
import models, schemas, crud, security
from database import SessionLocal, engine

# --- Logging Setup ---
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler(),                 # Console logs
        logging.FileHandler("app.log", mode="a") # File logs
    ]
)
logger = logging.getLogger(__name__)

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="LogPulse API")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, security.SECRET_KEY, algorithms=[security.ALGORITHM])
        email: str | None = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user = crud.get_user_by_email(db, email=email)
    if user is None:
        raise credentials_exception
    return user

@app.post("/users/", response_model=schemas.User)
def create_user_endpoint(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        logger.warning(f"Attempt to register duplicate email: {user.email}")
        raise HTTPException(status_code=400, detail="Email already registered")
    logger.info(f"User created: {user.email}")
    return crud.create_user(db=db, user=user)

@app.post("/token", response_model=schemas.Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = crud.get_user_by_email(db, email=form_data.username)
    if not user or not security.verify_password(form_data.password, user.hashed_password):
        logger.error(f"Failed login attempt for: {form_data.username}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = security.create_access_token(data={"sub": user.email})
    logger.info(f"User logged in: {user.email}")
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/logs/", response_model=schemas.Log)
def create_log_entry(log: schemas.LogCreate, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    logger.info(f"Log created by {current_user.email}: {log.message}")
    return crud.create_log(db=db, log=log)

@app.get("/logs/", response_model=list[schemas.Log])
def read_logs(skip: int = 0, limit: int = 100, search: str | None = None, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    logs = crud.get_logs(db=db, skip=skip, limit=limit, search=search)
    logger.info(f"Logs fetched by {current_user.email}, search={search}")
    return logs

@app.get("/users/me/", response_model=schemas.User)
def read_users_me(current_user: schemas.User = Depends(get_current_user)):
    logger.info(f"Current user fetched: {current_user.email}")
    return current_user

# ✅ New RBAC-protected endpoint
@app.delete("/logs/{log_id}")
def delete_log(
    log_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    if current_user.role != "admin":   # RBAC check
        logger.warning(f"Unauthorized delete attempt by {current_user.email}")
        raise HTTPException(status_code=403, detail="Not enough permissions")

    log = db.query(models.Log).filter(models.Log.id == log_id).first()
    if not log:
        logger.warning(f"Log {log_id} not found for delete")
        raise HTTPException(status_code=404, detail="Log not found")

    db.delete(log)
    db.commit()
    logger.info(f"Log {log_id} deleted by {current_user.email}")
    return {"detail": "Log deleted successfully"}
