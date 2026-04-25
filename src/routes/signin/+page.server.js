import { fail, redirect } from '@sveltejs/kit';

export const actions = {
    default: async ({ request, cookies, fetch }) => {
        const data = await request.formData();
        const email = data.get('email');
        const password = data.get('password');

        if (email === 'test@gmail.com' && password === '1234') {
            const mockUser = {
                customer_id: 999, 
                username: "testuser",
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
                return fail(400, { error: 'อีเมลหรือรหัสผ่านไม่ถูกต้อง', email });
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

            
            cookies.set('session_token', 'real-token-active', {
                path: '/',
                httpOnly: true,
                maxAge: 60 * 60 * 24
            });

        } catch (err) {
            
            if (err.status === 303 || err.status === 302) throw err; 
            
            console.error("Signin Error:", err);
            return fail(500, { error: 'เซิร์ฟเวอร์หลังบ้านมีปัญหา (เช็ค FastAPI)', email });
        }

        throw redirect(303, '/profile');
    }
};