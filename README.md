# Study Companion

A full-stack web app that takes your class notes, generates an instant summary, and creates fill-in-the-blank questions so you can self-test before an exam.

Built as a portfolio project — full-stack (React + FastAPI), with JWT auth, a real database, and a rule-based NLP feature that works out of the box with no external API keys.

## Why this project

- **Full-stack**: React frontend talking to a FastAPI backend over a REST API, with a SQL database and JWT-based auth.
- **Applied NLP, no API key required**: summaries and quiz questions are generated with a word-frequency extractive summarizer written from scratch (see `backend/summarizer.py`) — so anyone who clones this repo can run it immediately.
- **Room to grow**: swap the summarizer for a real LLM API call later, add spaced repetition, multi-user note sharing, etc. See [Ideas for extending](#ideas-for-extending).

## Tech stack

| Layer      | Tech                                   |
|------------|-----------------------------------------|
| Frontend   | React (Vite)                            |
| Backend    | FastAPI, Python                         |
| Database   | SQLite via SQLAlchemy (swap for Postgres in production) |
| Auth       | JWT (python-jose) + bcrypt-free password hashing (passlib/pbkdf2) |
| Summarization | Custom extractive algorithm (word-frequency sentence scoring) |

## Screenshots

_Add a screenshot or GIF here once you run it locally — this is the first thing recruiters look at._

## Project structure

```
study-companion/
├── backend/
│   ├── main.py          # FastAPI app & routes
│   ├── database.py      # SQLAlchemy models & session
│   ├── schemas.py        # Pydantic request/response models
│   ├── auth.py            # JWT + password hashing
│   ├── summarizer.py      # Extractive summarizer + quiz generator
│   └── requirements.txt
└── frontend/
    ├── src/
    │   ├── App.jsx
    │   ├── AuthScreen.jsx
    │   ├── NoteForm.jsx
    │   ├── NoteCard.jsx
    │   └── api.js
    └── package.json
```

## Running it locally

### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

The API is now running at `http://127.0.0.1:8000` (interactive docs at `/docs`).

### Frontend

```bash
cd frontend
npm install
cp .env.example .env          # defaults to the local backend URL above
npm run dev
```

Open the URL Vite prints (usually `http://localhost:5173`).

## How the summarizer works

No OpenAI/Anthropic key needed — `backend/summarizer.py` implements a classic extractive-summarization technique:

1. Split the note into sentences.
2. Score each word by frequency (ignoring stopwords).
3. Score each sentence by the average frequency-score of its words.
4. Return the highest-scoring sentences, in their original order.

The quiz generator uses the same word-frequency signal to find the most "information-dense" word in a sentence and blanks it out, producing a fill-in-the-blank question.

## Ideas for extending

- [ ] Swap the summarizer for a real LLM API call (OpenAI, Anthropic, etc.) and compare quality
- [ ] Add spaced-repetition scheduling for the quiz questions
- [ ] Support PDF upload instead of pasting text (`pypdf` or similar)
- [ ] Deploy: frontend on Vercel, backend on Render/Railway, swap SQLite for Postgres
- [ ] Add tests (pytest for backend, Vitest for frontend)
- [ ] Multi-user note sharing / study groups

## License

MIT — use this however you like.
