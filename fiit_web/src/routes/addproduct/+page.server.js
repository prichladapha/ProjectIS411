const API = 'http://localhost:8000';

export async function load({ fetch }) {
  let categories = [];
  try {
    const res = await fetch(`${API}/categories/`);
    if (res.ok) categories = await res.json();
  } catch {
    categories = [];
  }
  return { categories };
}
