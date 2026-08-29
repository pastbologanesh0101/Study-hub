from pydantic import BaseModel
from datetime import datetime


class UserCreate(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class NoteCreate(BaseModel):
    title: str
    content: str
    subject: str = "General"


class NoteOut(BaseModel):
    id: int
    title: str
    content: str
    subject: str
    summary: str
    created_at: datetime

    class Config:
        from_attributes = True


class SummaryOut(BaseModel):
    summary: str
    quiz: list[str]
