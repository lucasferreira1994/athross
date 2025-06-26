from pydantic import BaseModel
import uuid

class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    confirm_password: str

class LoginRequest(BaseModel):
    email: str
    password: str
    remember: bool

class LoginResponse(BaseModel):
    access_token: str
    token_type: str
    
class UserProfile(BaseModel):
    username: str
    email: str
    active: bool
    uuid: uuid.UUID