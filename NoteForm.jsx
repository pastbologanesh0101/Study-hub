import { useState } from "react";

const SUBJECTS = ["General", "Data Structures", "Operating Systems", "DBMS", "Computer Networks", "Maths"];

export default function NoteForm({ onSubmit, submitting }) {
  const [title, setTitle] = useState("");
  const [subject, setSubject] = useState("General");
  const [content, setContent] = useState("");

  function handleSubmit(e) {
    e.preventDefault();
    if (!title.trim() || !content.trim()) return;
    onSubmit({ title, subject, content });
    setTitle("");
    setContent("");
  }

  return (
    <form className="note-form" onSubmit={handleSubmit}>
      <h2>Add a note</h2>
      <div className="field-row">
        <label>
          Title
          <input value={title} onChange={(e) => setTitle(e.target.value)} placeholder="e.g. Deadlocks — Unit 3" required />
        </label>
        <label>
          Subject
          <select value={subject} onChange={(e) => setSubject(e.target.value)}>
            {SUBJECTS.map((s) => (
              <option key={s} value={s}>{s}</option>
            ))}
          </select>
        </label>
      </div>
      <label>
        Content
        <textarea
          value={content}
          onChange={(e) => setContent(e.target.value)}
          placeholder="Paste your notes here — a paragraph or two works best."
          rows={8}
          required
        />
      </label>
      <button type="submit" className="btn-primary" disabled={submitting}>
        {submitting ? "Summarizing…" : "Save & summarize"}
      </button>
    </form>
  );
}
