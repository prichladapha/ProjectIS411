<script>
  import { addToCart, cartStore } from '$lib/cart.svelte.js'
    let {data} = $props()
  
    let isInCart  = $derived(cartStore.items.some(c => c.name === data.product.name))
</script>

<div
  class="has-background-primary px-4 py-3 is-flex is-align-items-center is-justify-content-space-between"
  style="position:sticky; top:0; z-index:10;"
>
  <div class="is-flex is-align-items-center" style="gap:12px;">
    <button
      class="button is-ghost px-1"
      style="color:white;"
      onclick={() => history.back()}
    >
      <span class="icon"><i class="fas fa-arrow-left"></i></span>
    </button>
    <span class="has-text-white has-text-weight-bold is-size-6" style="letter-spacing:1px;">
      PRODUCT DETAIL
    </span>
  </div>
  <button class="button is-small is-white is-rounded" disabled>
    <span class="icon is-small"><i class="fas fa-cog"></i></span>
  </button>
</div>

<div class="container mt-5 px-4">
  <div class="columns">

    <div class="column is-5">
      <figure class="image is-1by1" style="border-radius: 12px; overflow: hidden;">
        <img src={data.product.img} alt={data.product.name} style="object-fit: cover; width: 100%;">
      </figure>
    </div>

    <div class="column is-7">
      <p class="is-size-6 has-text-grey has-text-weight-medium">
        <span class="icon is-small has-text-primary"><i class="fas fa-store"></i></span>
        {data.product.shop}
      </p>
      <h1 class="is-size-4 has-text-weight-bold mt-3">{data.product.name}</h1>
      <p class="is-size-3 has-text-weight-bold has-text-primary mt-2">฿ {data.product.price}</p>

      <hr>

      <p class="has-text-weight-bold">PRODUCT DESCRIPTION</p>
      <p class="is-size-6 mt-2">{data.product.detail}</p>

      <hr>

      <div class="columns is-mobile mt-3">
        <div class="column">
          <button class="button is-light is-fullwidth is-rounded">
            <span class="icon"><i class="fas fa-comment"></i></span>
            <span>CHAT</span>
          </button>
        </div>
        <div class="column">
          <button 
            class="button is-fullwidth is-rounded {isInCart ? 'is-danger is-light' : 'is-primary'}"
            onclick={() => addToCart(data.product)}
            disabled={isInCart}>
    
            <span class="icon"><i class={isInCart ? "fas fa-check" : "fas fa-cart-plus"}></i></span>
            <span>{isInCart ? 'Added' : 'ADD TO CART'}</span>
          </button>
        </div>
      </div>

      <a href= "/checkout">
      <button class = "button is-warning is-fullwidth is-rounded has-text-weight-bold mt-2">
        <span>PLACE ORDER</span>
        <span class="ml-2">฿ {data.product.price}</span>
      </button>
      </a>
    </div>
  </div>
</div>