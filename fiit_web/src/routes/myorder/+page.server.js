export const load = async ({ fetch }) => {
    try {
        // ดึงข้อมูล 2 เส้นพร้อมกัน (Orders กับ Customers)
        const [resOrders, resCustomers] = await Promise.all([
            fetch('http://127.0.0.1:8000/orders/'),
            fetch('http://127.0.0.1:8000/customers/') 
        ]);

        if (!resOrders.ok) return { orders: [], error: 'ดึงข้อมูลออเดอร์ไม่ได้' };

        const orders = await resOrders.json();
        
        // ถ้าดึงลูกค้าสำเร็จ ให้สร้าง Map จับคู่ ID -> ชื่อ
        let nameMap = {};
        if (resCustomers.ok) {
            const customers = await resCustomers.json();
            // เช็คด้วยนะว่าหลังบ้านเพื่อนมึงใช้ field 'customer_id' กับ 'username' หรือเปล่า ถ้าไม่ใช่ให้แก้ตรงนี้
            nameMap = Object.fromEntries(customers.map(c => [c.customer_id, c.username]));
        }

        // เอาชื่อไปยัดใส่ออเดอร์
        const finalOrders = orders.map(o => ({
            ...o,
            customer_name: nameMap[o.customer_id] || 'ไม่ระบุชื่อ'
        }));

        return { orders: finalOrders };

    } catch (err) {
        return { orders: [], error: 'ติดต่อเซิร์ฟเวอร์ไม่ได้' };
    }
};