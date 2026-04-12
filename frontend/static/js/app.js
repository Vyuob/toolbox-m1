/* PentestBox – app.js */

// ── Auth ────────────────────────────────────────────────
function getToken() {
  return localStorage.getItem('access_token');
}

function requireAuth() {
  if (!getToken()) {
    window.location.href = '/login';
  }
}

function logout() {
  localStorage.removeItem('access_token');
  localStorage.removeItem('username');
  window.location.href = '/login';
}

async function loadUserInfo() {
  const data = await apiFetch('/api/auth/me');
  if (!data) return;
  const initials = data.username.slice(0, 2).toUpperCase();
  const el = document.getElementById('user-avatar');
  const nameEl = document.getElementById('user-name');
  const roleEl = document.getElementById('user-role');
  if (el) el.textContent = initials;
  if (nameEl) nameEl.textContent = data.username;
  if (roleEl) roleEl.textContent = data.role;
}

// ── API fetch ────────────────────────────────────────────
async function apiFetch(path, options = {}) {
  const token = getToken();
  try {
    const res = await fetch(path, {
      ...options,
      headers: {
        'Content-Type': 'application/json',
        ...(token ? { 'Authorization': `Bearer ${token}` } : {}),
        ...(options.headers || {}),
      },
    });

    updateApiStatus(res.ok || res.status < 500);

    if (res.status === 401) {
      logout();
      return null;
    }
    if (!res.ok) {
      const err = await res.json().catch(() => ({}));
      throw new Error(err.detail || `HTTP ${res.status}`);
    }
    if (res.status === 204 || res.headers.get('content-length') === '0') return null;
    return await res.json();
  } catch (e) {
    updateApiStatus(false);
    if (e.name !== 'TypeError') throw e;
    return null;
  }
}

function updateApiStatus(ok) {
  const dot = document.getElementById('api-status');
  if (!dot) return;
  dot.classList.toggle('offline', !ok);
  dot.title = ok ? 'API connectée' : 'API hors ligne';
}

// ── Horloge ──────────────────────────────────────────────
function startClock() {
  function tick() {
    const el = document.getElementById('clock');
    if (el) el.textContent = new Date().toLocaleTimeString('fr-FR');
  }
  tick();
  setInterval(tick, 1000);
}

// ── Utils ────────────────────────────────────────────────
function formatDate(iso) {
  if (!iso) return '–';
  try {
    return new Intl.DateTimeFormat('fr-FR', {
      day: '2-digit', month: '2-digit', year: 'numeric',
      hour: '2-digit', minute: '2-digit',
    }).format(new Date(iso));
  } catch { return iso; }
}
