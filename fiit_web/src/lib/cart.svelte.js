// กำหนด URL ตรงนี้ที่เดียว เปลี่ยนง่ายครับขิม
const API_BASE_URL = "http://127.0.0.1:8000";

export const cartStore = $state({
    items: [],
    get total() {
        // กรองเอาเฉพาะชิ้นที่ลูกค้าเลือก (Selected) มาคำนวณเงิน
        return this.items
            .filter(item => item.selected)
            .reduce((sum, item) => sum + item.price, 0);
    },
    get count() {
        return this.items.length;
    },
    get selectedCount() {
        return this.items.filter(item => item.selected).length;
    }
});

export async function loadCart() {
    const cus_id = localStorage.getItem("current_user_id");
    if (!cus_id) return;

    try {
        const res = await fetch(`${API_BASE_URL}/cart/${cus_id}`);
        if (res.ok) {
            cartStore.items = await res.json();
        }
    } catch (err) {
        console.error("Failed to load cart:", err);
    }
}

export async function addToCart(product) {
    const cus_id = localStorage.getItem("current_user_id");

    if (!cus_id) {
        alert("Please sign in to add items to your cart!");
        window.location.href = "/signin";
        return;
    }

    const payload = {
        cus_id: parseInt(cus_id),
        product_id: product.product_id,
        qty: 1
    };

    try {
        const res = await fetch(`${API_BASE_URL}/cart/add`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });

        if (res.ok) {
            await loadCart();
            alert("Added to cart!");
        }
    } catch (err) {
        alert("Connection error. ");
    }
}

export async function removeFromCart(index) {
    const itemToRemove = cartStore.items[index];
    try {
        const res = await fetch(`${API_BASE_URL}/cart/remove/${itemToRemove.cartitem_id}`, {
            method: 'DELETE'
        });
        if (res.ok) await loadCart();
    } catch (err) {
        console.error(err);
    }
}

// ✨ ฟังก์ชันใหม่: สำหรับหน้า Checkout UI
export async function checkout() {
    const cus_id = localStorage.getItem("current_user_id");
    if (!cus_id) {
        alert("Please login again.");
        return;
    }

    if (!confirm("Confirm your order?")) return;

    try {
        const res = await fetch(`${API_BASE_URL}/orders/checkout/${cus_id}`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' }
        });

        if (res.ok) {
            const data = await res.json();
            alert("Order Successful! Order ID: " + data.order_id);
            
            // ล้างข้อมูลในตะกร้าหน้าเว็บให้ว่างเปล่า
            await loadCart(); 
            
            // ส่งกลับหน้าแรก หรือหน้าขอบคุณ
            window.location.href = "/"; 
        } else {
            const err = await res.json();
            alert("Error: " + err.detail);
        }
    } catch (err) {
        alert("Server connection failed.");
    }
}

export function isInCart(product) {
    if (!product) return false;
    return cartStore.items.some(c => c.product_id === product.product_id);
}