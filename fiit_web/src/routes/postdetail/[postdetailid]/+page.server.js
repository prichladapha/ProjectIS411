import { error } from '@sveltejs/kit';

/** @type {import('./$types').PageServerLoad} */
export async function load({ params, fetch }) {
    const id = params.postdetailid;
   
    // 1. เช็ค URL ให้ดี 
    const res = await fetch(`http://127.0.0.1:8000/posts/${id}`);
   
    if (!res.ok) {
        throw error(404, 'ไม่พบโพสต์ที่ต้องการ');
    }

    const data = await res.json();
   
    // 2. Mapping ข้อมูลให้ชื่อฟิลด์ตรงกับหน้า +page.svelte
    // โดยปกติ Backend จะส่งก้อนใหญ่มา เราต้องแปลงให้มี name, avatar, image เหมือนหน้า Feed
    return {
        post: {
            id: data.post_info?.id || data.id,
            name: data.author?.display_name || data.name,
            username: data.author?.username || data.username,
            avatar: data.author?.avatar || data.avatar,
            content: data.post_info?.content || data.content,
            image: data.post_info?.image_url || data.image,
            staticComments: data.staticComments || []
        }
    };
}