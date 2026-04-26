import { fail } from '@sveltejs/kit';

export const actions = {
    default: async ({ request, fetch }) => {
        const formData = await request.formData();
        
        const username = formData.get('name'); 
        const display_name = formData.get('display_name');
        const email = formData.get('email');
        const phone = formData.get('phone'); 
        const password = formData.get('password');
        const confirmPassword = formData.get('confirmPassword');
        
        if (password !== confirmPassword) {
            return fail(400, { 
                error: 'รหัสผ่านไม่ตรงกัน', 
                name: username, email, phone, display_name 
            });
        }

        try {
  
            const payload = [{
                "username": String(username),
                "email": String(email),
                "customer_phone": String(phone), 
                "password": String(password),
                "display_name": String(display_name || username), 
                "avatar": "" 
            }];

            const response = await fetch('http://127.0.0.1:8000/customers/', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });

            const result = await response.json();

            if (!response.ok) {
                let msg = 'สมัครสมาชิกไม่สำเร็จ';
                if (result.detail) {
                    msg = Array.isArray(result.detail) ? result.detail[0].msg : result.detail;
                }
                return fail(response.status, { error: msg, name: username, email, phone, display_name });
            }

            return { 
                success: true, 
                message: 'บันทึกข้อมูลเข้า Database เรียบร้อยแล้ว!' 
            };

        } catch (err) {
            return fail(500, { 
                error: 'ติดต่อเซิร์ฟเวอร์ไม่ได้ (รัน FastAPI หรือยัง?)', 
                name: username, email, phone, display_name 
            });
        }
    }
};