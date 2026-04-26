import { fail } from '@sveltejs/kit';

export const actions = {
    default: async ({ request, fetch }) => {
        const formData = await request.formData();
        
        const username = formData.get('name'); 
        const email = formData.get('email');
        const phone = formData.get('phone'); 
        const password = formData.get('password');
        const confirmPassword = formData.get('confirmPassword');
        const display_name = formData.get('display_name');

        if (password !== confirmPassword) {
            return fail(400, { error: 'รหัสผ่านไม่ตรงกัน', name: username, email, phone, display_name });
        }

        try {
            // สร้าง Object ตัวเดียว
            const singleCustomer = {
                username: String(username),
                email: String(email),
                customer_phone: String(phone),
                password: String(password),
                display_name: String(display_name || username),
                avatar: ""
            };

            // ✅ บังคับส่งเป็น Array แน่นอน 100% (ใส่ก้ามปูครอบไว้เลย)
            const finalPayload = [singleCustomer];

            const response = await fetch('http://127.0.0.1:8000/customers/', {
                method: 'POST',
                headers: { 
                    'Content-Type': 'application/json',
                    'Accept': 'application/json' 
                },
                body: JSON.stringify(finalPayload)
            });

            const result = await response.json();

            if (!response.ok) {
                // ถ้ายังเฟล ให้พ่น Error จริงๆ ออกมาดู (ฆ่าผี [object Object])
                const errorDetail = Array.isArray(result.detail) ? result.detail[0].msg : result.detail;
                return fail(response.status, { 
                    error: `หลังบ้านด่าว่า: ${errorDetail}`, 
                    name: username, email, phone 
                });
            }

            return { success: true, message: 'สำเร็จ! ข้อมูลเข้า Database แล้ว' };

        } catch (err) {
            return fail(500, { error: 'ติดต่อ Server ไม่ได้', name: username });
        }
    }
};