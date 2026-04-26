export async function load({ cookies }) {
    const raw = cookies.get('user_data');
    const user = raw ? JSON.parse(raw) : null;
    return { user };
}