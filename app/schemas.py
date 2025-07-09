from pydantic import BaseModel, Field, field_validator
import re


class UserCreate(BaseModel):
    username: str
    password: str = Field(..., min_length=8)
   
    @field_validator('password')
    def validate_password(cls, v):
        if not re.search(r"[A-Z]", v):
            raise ValueError("Password must contain at least one uppercase letter")
        if not re.search(r"[a-z]", v):
            raise ValueError("Password must contain at least one lowercase letter")
        if not re.search(r"[0-9]", v):
            raise ValueError("Password must contain at least one digit")
        if not re.search(r"[!@#\$%\^&\*]", v):
            raise ValueError("Password must contain at least one special character (!@#$%^&*)")
        return v

class UserLogin(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    id: int
    username: str

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str
