from pydantic import BaseModel

from Models.models import UserRole


class Login(BaseModel):
    email: str
    password: str
class Token(BaseModel):
    access_token: str
    token_type: str
class TokenData(BaseModel):
    id: int | None = None
    role:UserRole | None = None
    email: str | None = None
