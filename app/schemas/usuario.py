from datetime import datetime

from sqlmodel import SQLModel


class UserBase(SQLModel):
    email: str


class UserCreate(UserBase):
    password: str


class UserRead(UserBase):
    id: int
    created_at: datetime
