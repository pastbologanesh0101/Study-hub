import { useState } from "react";
import { api } from "./api";

export default function NoteCard({ note, token, onDelete }) {
  const [quiz, setQuiz] = useState(null);
  const [loadingQuiz, setLoadingQuiz] = useState(false);
  const [expanded, setExpanded] = useState(false);

  async function loadQuiz() {
    if (quiz) {
      setQuiz(null);
      return;
    }
    setLoadingQuiz(true);
    try {
      const result = await api.getQuiz(token, note.id);
      setQuiz(result.quiz);
    } catch {
      setQuiz([]);
    } finally {
      setLoadingQuiz(false);
    }
  }

  return (
    <article className="note-card">
      <div className="note-card-header">
        <span className="subject-tag">{note.subject}</span>
        <button className="icon-btn" onClick={() => onDelete(note.id)} aria-label="Delete note" title="Delete note">
          ✕
        </button>
      </div>
      <h3>{note.title}</h3>

      <div className="note-summary">
        <span className="eyebrow">Summary</span>
        <p>{note.summary}</p>
      </div>

      <button className="link-btn" onClick={() => setExpanded(!expanded)}>
        {expanded ? "Hide full note" : "Show full note"}
      </button>
      {expanded && <p className="note-full-content">{note.content}</p>}

      <button className="btn-secondary" onClick={loadQuiz} disabled={loadingQuiz}>
        {loadingQuiz ? "Generating…" : quiz ? "Hide self-test" : "Self-test me"}
      </button>

      {quiz && (
        <ul className="quiz-list">
          {quiz.length === 0 && <li>Not enough content to generate questions.</li>}
          {quiz.map((q, i) => (
            <li key={i}>{q}</li>
          ))}
        </ul>
      )}
    </article>
  );
}
