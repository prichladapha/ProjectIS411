export async function load({ fetch }) {
  const res = await fetch('http://localhost:8000/posts/');

  if (!res.ok) {
    return { posts: [] };
  }

  const rawPosts = await res.json();

  // แปลงข้อมูล (Mapping) ให้ใช้ง่ายๆ
  const posts = rawPosts.map(p => ({
    id: p.id,
    name: p.name,
    username: p.username,
    avatar: p.avatar,
    content: p.content,
    image: p.image, // จาก Backend แปลง image_url เป็น image แล้ว
    likes: p.likes,
    comments_count: p.comments // จำนวนคอมเมนต์
  }));

  return { posts };
}
