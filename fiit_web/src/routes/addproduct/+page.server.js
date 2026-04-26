const API = 'http://localhost:8000';

/** @type {import('./$types').PageServerLoad} */
export async function load({ cookies }) {
  // อ่าน user จาก cookie ที่ signin set ไว้
  const raw = cookies.get('user_data');
  const user = raw ? JSON.parse(raw) : null;

  // ดึง categories จาก API
  let categories = [];
  try {
    const res = await fetch(`${API}/categories/`);
    if (res.ok) categories = await res.json();
  } catch {
    categories = [];
  }

  return { user, categories };
}