import { useEffect, useState } from "react";
import AuthScreen from "./AuthScreen";
import NoteForm from "./NoteForm";
import NoteCard from "./NoteCard";
import { api } from "./api";
import "./App.css";

export default function App() {
  const [token, setToken] = useState(null);
  const [username, setUsername] = useState("");
  const [notes, setNotes] = useState([]);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    if (token) refreshNotes();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [token]);

  async function refreshNotes() {
    try {
      setNotes(await api.listNotes(token));
    } catch (err) {
      setError(err.message);
    }
  }

  async function handleCreateNote(note) {
    setSubmitting(true);
    setError("");
    try {
      const created = await api.createNote(token, note);
      setNotes((prev) => [created, ...prev]);
    } catch (err) {
      setError(err.message);
    } finally {
      setSubmitting(false);
    }
  }

  async function handleDeleteNote(id) {
    try {
      await api.deleteNote(token, id);
      setNotes((prev) => prev.filter((n) => n.id !== id));
    } catch (err) {
      setError(err.message);
    }
  }

  function handleLogout() {
    setToken(null);
    setUsername("");
    setNotes([]);
  }

  if (!token) {
    return <AuthScreen onAuth={(t, u) => { setToken(t); setUsername(u); }} />;
  }

  return (
    <div className="app-shell">
      <header className="app-header">
        <div className="brand-mark small">SC</div>
        <div>
          <h1>Study Companion</h1>
          <p className="muted">Signed in as {username}</p>
        </div>
        <button className="link-btn logout" onClick={handleLogout}>Log out</button>
      </header>

      {error && <div className="error-banner">{error}</div>}

      <main className="app-main">
        <section>
          <NoteForm onSubmit={handleCreateNote} submitting={submitting} />
        </section>

        <section>
          <h2>Your notes {notes.length > 0 && <span className="count">({notes.length})</span>}</h2>
          {notes.length === 0 ? (
            <p className="empty-state">No notes yet — add your first one to get a summary and self-test questions.</p>
          ) : (
            <div className="note-grid">
              {notes.map((note) => (
                <NoteCard key={note.id} note={note} token={token} onDelete={handleDeleteNote} />
              ))}
            </div>
          )}
        </section>
      </main>
    </div>
  );
}
