export async function load() {
  const res = await fetch('http://localhost:8000/categories/');

  if (!res.ok) return { categories: [] };

  const categories = await res.json();
  return { categories };
}