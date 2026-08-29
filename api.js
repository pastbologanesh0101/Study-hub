const API_URL = import.meta.env.VITE_API_URL || "http://127.0.0.1:8000";

function authHeaders(token) {
  return token ? { Authorization: `Bearer ${token}` } : {};
}

async function handle(res) {
  if (!res.ok) {
    const body = await res.json().catch(() => ({}));
    throw new Error(body.detail || `Request failed (${res.status})`);
  }
  if (res.status === 204) return null;
  return res.json();
}

export const api = {
  signup: (username, password) =>
    fetch(`${API_URL}/auth/signup`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username, password }),
    }).then(handle),

  login: (username, password) =>
    fetch(`${API_URL}/auth/login`, {
      method: "POST",
      headers: { "Content-Type": "application/x-www-form-urlencoded" },
      body: new URLSearchParams({ username, password }),
    }).then(handle),

  listNotes: (token) =>
    fetch(`${API_URL}/notes`, { headers: authHeaders(token) }).then(handle),

  createNote: (token, note) =>
    fetch(`${API_URL}/notes`, {
      method: "POST",
      headers: { "Content-Type": "application/json", ...authHeaders(token) },
      body: JSON.stringify(note),
    }).then(handle),

  deleteNote: (token, id) =>
    fetch(`${API_URL}/notes/${id}`, {
      method: "DELETE",
      headers: authHeaders(token),
    }).then(handle),

  getQuiz: (token, id) =>
    fetch(`${API_URL}/notes/${id}/quiz`, { headers: authHeaders(token) }).then(handle),
};
