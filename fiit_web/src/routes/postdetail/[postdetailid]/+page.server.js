import { error, fail } from '@sveltejs/kit';


//ดึงข้อมูลโพสต์เฉพาะเจาะจงตาม ID และจัดการการส่งคอมเมนต์
/** @type {import('./$types').PageServerLoad} */
export async function load({ params, fetch }) {
    // 1. รับค่า params: 'postdetailid' มาจากชื่อโฟลเดอร์ [postdetailid]
    const { postdetailid } = params;
    const url = `http://localhost:8000/posts/${postdetailid}`;


    try {
        console.log(`Fetching data from API: ${url}`);
        const res = await fetch(url);


        // 2. ตรวจสอบ Error: ถ้าหาโพสต์ไม่เจอให้ส่งไปหน้า 404 Error
        if (!res.ok) {
            console.error(`Fetching data failed with status: ${res.status}`);
            throw error(res.status, 'ไม่พบโพสต์ที่ต้องการ หรือเกิดข้อผิดพลาดที่ Server');
        }


        const data = await res.json();
       
        // 3. จัดกลุ่มข้อมูล: แยกข้อมูลโพสต์และคอมเมนต์ส่งกลับไปให้ UI
        return {
            post: {
                id: data.post_info.id,
                content: data.post_info.content,
                image: data.post_info.image,
                name: data.post_info.name,
                username: data.post_info.username,
                avatar: data.post_info.avatar,
                likes: data.post_info.likes,
                reposts: data.post_info.reposts,
                shares: data.post_info.shares,
                staticComments: data.static_comments || []
            }
        };


    } catch (err) {
        if (err.status) throw err;
        console.error('Unexpected Error:', err.message);
        throw error(500, 'Internal Server Error');
    }
}


/** @type {import('./$types').Actions} */
export const actions = {
    default: async ({ request, params, fetch }) => {
        const formData = await request.formData();
        const text = formData.get('commentText');
        const customer_id = formData.get('customer_id');

        if (!text || text.toString().trim() === '') {
            return fail(400, { error: 'กรุณาพิมพ์ข้อความก่อนตอบกลับ' });
        }

        try {
            const res = await fetch(`http://localhost:8000/posts/${params.postdetailid}/comments`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    text: text.toString(), 
                    customer_id: parseInt(customer_id.toString()),
                    post_id: parseInt(params.postdetailid)
                })
            });

            if (res.ok) {
                const newComment = await res.json();
                return { success: true, newComment };
            }

            // ถ้าไม่ ok ให้ดู status จาก console ของ svelte
            const errorData = await res.json().catch(() => ({}));
            console.error('Backend Error:', errorData);
            return fail(500, { error: 'Backend ปฏิเสธการส่งข้อมูล (Check URL/Field name)' });

        } catch (e) {
            console.error('Fetch Error:', e);
            return fail(500, { error: 'เชื่อมต่อกับ Server ไม่ได้ (Server ล่มหรือ URL ผิด)' });
        }
    }
};