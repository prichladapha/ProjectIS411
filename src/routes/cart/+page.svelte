<script>
  import { cartStore, removeFromCart } from '$lib/cart.svelte.js';
  import CartItem from '$lib/component/CartItem.svelte';
  // จัดกลุ่มสินค้าตามชื่อร้าน (Shop)
  // เราจะเก็บ originalIndex ไว้ด้วย เพื่อให้ปุ่มลบยังทำงานได้ถูกต้อง
  let groupedShops = $derived([...new Set(cartStore.items.map(item => item.shop || "ทั่วไป"))]);
</script>

<section class="section pt-3">
  <div class="container">
    
    <nav class="level is-mobile mt-5">
      <div class="level-left">
        <div class="level-item">
          <h1 class="title is-4">Shopping Cart</h1>
        </div>
      </div>
    </nav>

    {#if cartStore.items.length === 0}
      <div class="box has-text-centered py-6">
        <p class="has-text-grey">Your cart is currently empty.</p>
        <a href="/" class="button is-primary is-light mt-3">Continue Shopping</a>
      </div>
    {:else}
      {#each groupedShops as shopname}
      <div class="shop-group mb-5">
      <div class="is-flex is-vcentered mb-2 px-2">
      <span class="icon has-text-primary mr-2">
        <i class="fas fa-store"></i>
      </span>
      <strong class="is-size-6">{shopname}</strong>
    </div>

    <div class="box p-4">
      {#each cartStore.items as _, index}
        {#if (cartStore.items[index].shop || "ทั่วไป") === shopname}
              <CartItem 
                bind:item={cartStore.items[index]} 
                {index} 
                onRemove={removeFromCart} 
              />
            {/if}
      {/each}
    </div>
  </div>
{/each}

      <div class="box has-background-primary has-text-white">
        <div class="level is-mobile">
          <div class="level-left">
            <div class="level-item">
              <div>
                <p class="heading">Total Amount</p>
                <p class="title is-4 has-text-white">฿ {cartStore.total.toLocaleString()}</p>
              </div>
            </div>
          </div>
          <div class="level-right">
            <div class="level-item">
              <a
              href="/checkout" 
              class="button is-warning is-rounded has-text-weight-bold {cartStore.selectedCount === 0 ? 'is-disabled' : ''}"
              aria-disabled={cartStore.selectedCount === 0}
              >
                CHECKOUT ({cartStore.selectedCount})
            </a>
            </div>
          </div>
        </div>
      </div>
    {/if}
  </div>
</section>

<style>
  .is-disabled {
    opacity: 0.5;               
    cursor: not-allowed;       
    pointer-events: none;        
    background-color: #ccc !important;                                                               
    border-color: #ccc !important;
  }
</style>