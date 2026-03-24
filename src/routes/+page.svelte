<script>
  import {addToCart, cartStore} from '$lib/cart.svelte.js';
  import {products, categories} from '$lib/Product.js';
  import ProductCard from '$lib/component/ProductCard.svelte';
  
  let activeCategory = $state(null);
  let searchQuery = $state("");

   function toggleCategory(cat) {
    activeCategory = activeCategory === cat ? null : cat;
  }

  let filteredProducts = $derived(
    products.filter(p => {
    // เช็คว่าชื่อสินค้ามีคำที่ค้นหาไหม (แปลงเป็นตัวพิมพ์เล็กทั้งคู่เพื่อให้หาง่าย)
      const matchesSearch = p.name.toLowerCase().includes(searchQuery.toLowerCase());
      // เช็คว่าตรงกับหมวดหมู่ที่เลือกไหม (ถ้าไม่ได้เลือก ให้ผ่านหมด)
      const matchesCategory = activeCategory === null || p.category === activeCategory;
      
      return matchesSearch && matchesCategory;
    })
  );
  function isInCart(item) {
    return cartStore.items.some(c => c.name === item.name);
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
  {#each categories as cat}
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
  {#each filteredProducts as item}
    <div class="column is-4">
      <ProductCard 
        {item}
        isInCart={isInCart(item)}
        onAddToCart={() => addToCart(item)}
      />
    </div>
  {/each}
</div>
</div>

