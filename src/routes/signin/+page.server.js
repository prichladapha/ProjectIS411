import { fail, redirect } from '@sveltejs/kit';

export const actions = {
    default: async ({ request, cookies, fetch }) => {
        const formData = await request.formData();
        const email = formData.get('email');
        const password = formData.get('password');

        if (!email || !password) {
            return fail(400, { error: 'กรุณากรอกอีเมลและรหัสผ่าน', email });
        }

        if (email === 'test@gmail.com' && password === '1234') {
            const mockUser = {
                customer_id: 999, 
                username: "testuser (Mockup)",
                email: "test@gmail.com"
            };

            cookies.set('user_data', JSON.stringify(mockUser), {
                path: '/',
                maxAge: 60 * 60 * 24,
                httpOnly: false 
            });

            throw redirect(303, '/profile');
        }

        try {
            const response = await fetch('http://127.0.0.1:8000/Signin', { 
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ email, password })
            });

            if (!response.ok) {
                const errorDetail = await response.json();
                return fail(401, { error: errorDetail.detail || 'อีเมลหรือรหัสผ่านไม่ถูกต้อง', email });
            }

            const result = await response.json();

            cookies.set('user_data', JSON.stringify({
                customer_id: result.customer_id,
                username: result.username
            }), {
                path: '/',
                maxAge: 60 * 60 * 24,
                httpOnly: false 
            });

            cookies.set('session_token', 'real-db-session', {
                path: '/',
                httpOnly: true,
                maxAge: 60 * 60 * 24
            });

        } catch (err) {

            if (err.status === 303 || err.status === 302) throw err; 
            
            console.error("Database Connection Error:", err);
            return fail(500, { error: 'ติดต่อเซิร์ฟเวอร์ Database ไม่ได้ (FastAPI รันอยู่ไหม?)', email });
        }

        throw redirect(303, '/profile');
    }
};