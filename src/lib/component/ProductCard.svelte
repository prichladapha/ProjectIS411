<script>
  let { item, onAddToCart, isInCart } = $props();
</script>

<div class="box p-0 has-background-light" style="overflow: hidden;">
  <figure class="image is-1by1">
    <img src={item.img} alt={item.name} style="object-fit: cover;">
  </figure>
  <div class="p-3">
    <p class="is-size-6 has-text-weight-semibold mb-1">{item.name}</p>
    <p class="is-size-7 mb-3">{item.detail}</p>
    <p class="has-text-primary has-text-weight-bold is-size-5">฿ {item.price}</p>
    <p class="is-size-7 has-text-grey mt-1">
      <span class="icon is-small"><i class="fas fa-store"></i></span>
      {item.shop}
    </p>
    <button 
      class="button is-fullwidth is-rounded has-text-weight-bold mt-2 {isInCart ? 'is-light is-danger' : 'is-primary'}"
      onclick={onAddToCart}
      disabled={isInCart}
    >
      <span class="icon is-small">
        <i class="fas {isInCart ? 'fa-check' : 'fa-cart-plus'}"></i>
      </span>
      <span>{isInCart ? 'Added' : 'Add to Cart'}</span>
    </button>
  </div>
</div>