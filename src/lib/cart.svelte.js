// สร้าง Object ก้อนเดียวที่เก็บทั้งข้อมูลและฟังก์ชัน
export const cartStore = $state({
    items: [], // รายการสินค้าในตะกร้า
    
    // ใช้ get เพื่อทำหน้าที่เหมือน $derived (คำนวณอัตโนมัติ)
    get total() {
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

// ฟังก์ชันสำหรับเพิ่มสินค้า
export function addToCart(product) {
    cartStore.items.push({ ...product, selected: true });
    console.log("เพิ่มสินค้าแล้ว:", product.name);
}

export function removeFromCart(index) {
    // ใช้ .splice เพื่อลบออก 1 ตำแหน่งตาม index ที่ส่งมา
    cartStore.items.splice(index, 1);
    console.log("ลบสินค้าตำแหน่งที่:", index);
}

export function isInCart(product) {
  return cartStore.items.some(c => c.name === product.name);
}

