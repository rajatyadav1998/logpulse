from pydantic import BaseModel, ConfigDict
import datetime

# --- Log Schemas ---
class LogBase(BaseModel):
    message: str

class LogCreate(LogBase):
    pass

class Log(LogBase):
    id: int
    timestamp: datetime.datetime

    # ✅ Replace deprecated Config with ConfigDict
    model_config = ConfigDict(from_attributes=True)


# --- User Schemas ---
class UserBase(BaseModel):
    email: str

class UserCreate(UserBase):
    password: str
    role: str = "user"   # ✅ default role when creating

class User(UserBase):
    id: int
    role: str            # ✅ role visible in responses

    model_config = ConfigDict(from_attributes=True)


# --- Token Schemas ---
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: str | None = None
