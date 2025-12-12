from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class UserBase(BaseModel):
    name: str = Field(..., min_length=1)
    surname: str = Field(..., min_length=1)
    dni: str = Field(..., min_length=1)
    address: str = Field(..., min_length=1)

class UserCreate(UserBase):
    pass

class UserUpdate(BaseModel):
    id: int
    name: Optional[str] = None
    surname: Optional[str] = None
    dni: Optional[str] = None
    address: Optional[str] = None

class UserFilter(BaseModel):
    name: Optional[str] = None
    surname: Optional[str] = None
    dni: Optional[str] = None

class UserResponse(UserBase):
    id: int
    created_at: str
    updated_at: str
