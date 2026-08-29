from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from database import init_db, get_db, User, Note
from schemas import UserCreate, Token, NoteCreate, NoteOut, SummaryOut
from auth import hash_password, verify_password, create_access_token, get_current_user
from summarizer import summarize, generate_quiz

app = FastAPI(title="VIT Study Companion API")

# Allow the local Vite dev server (and any origin in dev) to call this API.
# Tighten allow_origins to your deployed frontend URL in production.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup():
    init_db()


@app.get("/")
def root():
    return {"status": "ok", "service": "VIT Study Companion API"}


# ---------- Auth ----------

@app.post("/auth/signup", response_model=Token)
def signup(user_in: UserCreate, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.username == user_in.username).first()
    if existing:
        raise HTTPException(status_code=400, detail="Username already taken")

    user = User(username=user_in.username, hashed_password=hash_password(user_in.password))
    db.add(user)
    db.commit()
    db.refresh(user)

    token = create_access_token({"sub": user.username})
    return Token(access_token=token)


@app.post("/auth/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect username or password")

    token = create_access_token({"sub": user.username})
    return Token(access_token=token)


# ---------- Notes ----------

@app.post("/notes", response_model=NoteOut)
def create_note(note_in: NoteCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    note = Note(
        title=note_in.title,
        content=note_in.content,
        subject=note_in.subject,
        summary=summarize(note_in.content),
        owner_id=user.id,
    )
    db.add(note)
    db.commit()
    db.refresh(note)
    return note


@app.get("/notes", response_model=list[NoteOut])
def list_notes(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    return db.query(Note).filter(Note.owner_id == user.id).order_by(Note.created_at.desc()).all()


@app.get("/notes/{note_id}", response_model=NoteOut)
def get_note(note_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    note = db.query(Note).filter(Note.id == note_id, Note.owner_id == user.id).first()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return note


@app.delete("/notes/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_note(note_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    note = db.query(Note).filter(Note.id == note_id, Note.owner_id == user.id).first()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    db.delete(note)
    db.commit()
    return None


@app.get("/notes/{note_id}/quiz", response_model=SummaryOut)
def get_quiz(note_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    note = db.query(Note).filter(Note.id == note_id, Note.owner_id == user.id).first()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return SummaryOut(summary=note.summary, quiz=generate_quiz(note.content))
