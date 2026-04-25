<script>
  import {addToCart, cartStore} from '$lib/cart.svelte.js';
  import ProductCard from '$lib/component/ProductCard.svelte';

  import { page } from '$app/stores'

  let { data } = $props();

  let products = $state(data.products);
  let activeCategory = $state(null);
  let searchQuery = $state("");

  // ---- Svelte Action: ส่ง search/filter ไป POST /products/search ----
  function searchAction(node) {
    async function doSearch() {
      const body = {
        query: searchQuery || null,
        category_id: activeCategory || null,
        page: 1,
        page_size: 20
      };

      const res = await fetch('http://localhost:8000/products/search', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body)
      });

       if (res.ok) {
        const result = await res.json();
        products = result.products;   // อัพเดต products ที่แสดง
      }
    }

     // ฟังการกด Enter ในช่อง search
    node.addEventListener('search-submit', doSearch);
    return {
      destroy() {
        node.removeEventListener('search-submit', doSearch);
      }
    };
  }
  
  // trigger action เมื่อ category เปลี่ยน
  function toggleCategory(cat) {
    activeCategory = activeCategory === cat ? null : cat;
    triggerSearch(activeCategory);  // ส่งไป API ทันทีที่เปลี่ยน category
  }

  // filter เฉพาะ client-side (ขณะพิมพ์) — ใช้ field ของ API
  let filteredProducts = $derived(
    products.filter(p => {
    // เช็คว่าชื่อสินค้ามีคำที่ค้นหาไหม (แปลงเป็นตัวพิมพ์เล็กทั้งคู่เพื่อให้หาง่าย)
      const matchesSearch = p.pname.toLowerCase().includes(searchQuery.toLowerCase());
      // เช็คว่าตรงกับหมวดหมู่ที่เลือกไหม (ถ้าไม่ได้เลือก ให้ผ่านหมด)
      return matchesSearch;
    })
  );

  async function triggerSearch(currentCategory = activeCategory) {
    // ✅ ถ้าไม่มี category และไม่มี searchQuery ให้ reset กลับ data เดิมเลย
    if (!currentCategory && !searchQuery) {
        products = data.products;
        return;
    }

    const categoryId = currentCategory
        ? Object.entries(data.categoryMap).find(([id, name]) => name === currentCategory)?.[0]
        : null;

    const body = {
        query: searchQuery || null,
        category_id: categoryId ? parseInt(categoryId) : null,
        page: 1,
        page_size: 20
    };

    const res = await fetch('http://localhost:8000/products/search', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body)
    });

    if (res.ok) {
        const result = await res.json();
        products = result.products;
    }
}

  // map field API → format ที่ ProductCard ใช้
  function toCardItem(p) {
    return {
      name: p.pname,
      price: p.price,
      shop: p.brand,
      detail: p.description,
      img: p.image_url ?? 'https://placehold.co/400x400',
      category: p.categoryID,
      product_id: p.product_id
    };
  }
  
  function isInCart(item) {
    return cartStore.items.some(c => c.product_id=== item.product_id);
  }
  
</script>

<div class="container pt-5">
  <div class="level-item mt-3" style="width:100%;">
        <div class="field has-addons" style="width:100%;">
          <p class="control is-expanded">
            <input 
            class="input is-rounded " 
            type="text" 
            placeholder="Search..."
            bind:value={searchQuery}>
          </p>
          <p class="control">
            <button class="button is-primary is-rounded ">
              <span class="icon is-small">
                <i class="fas fa-search"></i>
              </span>
            </button>
          </p>
        </div>
  </div>



  <p class="is-size-5 has-text-weight-bold mt-5">CATEGORY</p>


<div class="columns is-mobile is-variable is-2 mt-2">
  {#each data.categories as cat}
    <div class="column">
      <button
        class="button is-rounded is-fullwidth {activeCategory === cat ? 'is-warning has-text-weight-bold' : 'is-light'}"
        onclick={() => toggleCategory(cat)}
      >
        {cat}
      </button>
    </div>
  {/each}
</div>



<p class="is-size-5 has-text-weight-bold mt-5">RECOMMENDED FOR YOU</p>

</div>

<div class="container pt-5">
<div class="columns is-mobile is-multiline mt-1">
  {#each filteredProducts.map(toCardItem) as item}
    <div class="column is-4">
        <ProductCard 
          item={item}
          isInCart={isInCart(item)}
          onAddToCart={(e) => {
          e.preventDefault();
          e.stopPropagation();
          if (!data.user) {
              alert("Please sign in to add items to your cart!");
              return;
            }
          addToCart(item);
         }} 
        />
    </div>
  {/each}
</div>
</div>