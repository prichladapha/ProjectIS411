import { fail } from '@sveltejs/kit';


/** @type {import('./$types').PageServerLoad} */
export async function load({ fetch }) {
    const url = 'http://localhost:8000/posts/';
   
    try {
        // 1. ดึงข้อมูล: ใช้ fetch() ยิงไปที่ Backend Python 
        const res = await fetch(url);
       
        // 2. เช็คสถานะ: ถ้า Backend พังหรือหาไม่เจอ ให้กระโดดไปส่วน catch (Error Handling)
        if (!res.ok) {
            throw new Error(`Response status: ${res.status}`);
        }


        // 3. แปลงข้อมูล: เปลี่ยนข้อมูลจาก JSON ของ Backend มาเป็น Object ของ JS
        const posts = await res.json();


        // 4. Mapping ข้อมูล: ปรับชื่อตัวแปรให้ตรงกับที่หน้า .svelte ต้องการใช้งาน (Data Transformation)
        return {
            posts: posts.map(post => ({
                id: post.id,
                content: post.content,
                image: post.image,
                name: post.name,
                username: post.username,
                avatar: post.avatar,
                likes: post.likes,
                comments: post.comments_count,
                reposts: post.reposts,
                shares: post.shares
            }))
        };
    } catch (err) {
        // 5. กรณี Error: ถ้าโหลดไม่ได้ ให้คืนค่าลิสต์ว่าง เพื่อไม่ให้หน้าเว็บล่ม (Graceful Degradation)
        console.error('Error loading posts:', err.message);
        return { posts: [] };
    }
}


//ทำงานเมื่อผู้ใช้กดปุ่ม "Post" (ปุ่ม Submit ของฟอร์ม)
/** @type {import('./$types').Actions} */
export const actions = {
    // ชื่อ action คือ createPost (เรียกใช้ในหน้าบ้านด้วย action="?/createPost")
    createPost: async ({ request, fetch }) => {
        // 1. รับข้อมูล: แกะข้อมูลจากฟอร์มที่ส่งมา (เหมือนบทเรียน 12)
        const formData = await request.formData();
        const content = formData.get('content');
        const customer_id = formData.get('customer_id');
        const image_url = formData.get('image_url') || "";


        // 2. Validation: ตรวจสอบข้อมูลเบื้องต้น ถ้าว่างให้ส่ง error กลับไปแจ้งผู้ใช้
        // (ใช้ fail() 
        if (!content || content.toString().trim() === '') {
            return fail(400, { error: 'กรุณากรอกเนื้อหาโพสต์' });
        }


        try {
            // 3. ส่งข้อมูลไป Backend: ยิง POST request เพื่อบันทึกข้อมูลลงฐานข้อมูลจริง
            const res = await fetch('http://127.0.0.1:8000/posts/', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    content: content.toString(),
                    customer_id: parseInt(customer_id.toString()),
                    image_url: image_url.toString()
                })
            });


            // 4. ส่งผลลัพธ์กลับหน้าบ้าน: ถ้าสำเร็จส่ง success ถ้าไม่สำเร็จส่ง error
            if (res.ok) return { success: true };
            return fail(500, { error: 'Server Error' });
        } catch (e) {
            // กรณีต่อ Server ไม่ติด (เช่น ลืมเปิด Backend Python)
            return fail(500, { error: 'Connection failed' });
        }
    }
};

