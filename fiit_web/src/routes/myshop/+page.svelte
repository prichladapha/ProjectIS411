<script>
  import { goto } from '$app/navigation';

  let { data } = $props();

  // ── ข้อมูล shop จาก load function ──
  let shop = $state(data?.shop ?? {
    name: 'cutiecat shop',
    verified: true,
    followers: 128,
    following: 47,
    avatar_url: null,
  });

  let stats = $state(data?.stats ?? {
    toShip: 3,
    cancelled: 1,
    returned: 0,
    review: 5,
  });

  let products = $state(data?.products ?? [
    { id: 1, pname: 'Vintage Denim Jacket', price: 590, product_status: 'available', brand: 'Levi\'s' },
    { id: 2, pname: 'Floral Midi Skirt',    price: 320, product_status: 'available', brand: 'Zara'   },
    { id: 3, pname: 'Oversized Tee (Black)',price: 180, product_status: 'sold',      brand: 'Uniqlo' },
  ]);

  let orders = $state(data?.orders ?? [
    { id: 1001, product_name: 'Vintage Denim Jacket', status: 'to_ship',  price: 590 },
    { id: 1002, product_name: 'Floral Midi Skirt',    status: 'pending',  price: 320 },
    { id: 1003, product_name: 'Oversized Tee (Black)',status: 'complete', price: 180 },
  ]);

  let activeTab = $state('products'); // 'products' | 'orders'

  function statusColor(status) {
    if (status === 'available') return 'is-success is-light';
    if (status === 'sold')      return 'is-danger is-light';
    return 'is-warning is-light';
  }

  function orderStatusLabel(status) {
    const map = { to_ship: 'To Ship', pending: 'Pending', complete: 'Complete', cancelled: 'Cancelled' };
    return map[status] ?? status;
  }

  function orderStatusColor(status) {
    if (status === 'to_ship')   return 'is-primary is-light';
    if (status === 'complete')  return 'is-success is-light';
    if (status === 'cancelled') return 'is-danger is-light';
    return 'is-warning is-light';
  }
</script>

<!-- ── STICKY HEADER ── -->
<div
  class="has-background-primary px-4 py-3 is-flex is-align-items-center is-justify-content-space-between"
  style="position:sticky; top:0; z-index:10;"
>
  <div class="is-flex is-align-items-center" style="gap:12px;">
  <button
    class="button is-ghost px-1"
    style="color:white;"
    onclick={() => goto('/myshop')}
  >
    <span class="icon"><i class="fas fa-arrow-left"></i></span>
  </button>
  <span class="has-text-white has-text-weight-bold is-size-6" style="letter-spacing:1px;">
    SHOP PROFILE
  </span>
</div>
  <button class="button is-small is-white is-rounded" onclick={() => goto('/settings')}>
    <span class="icon is-small"><i class="fas fa-cog"></i></span>
  </button>
</div>

<section class="section pt-4 pb-6">
  <div class="container" style="max-width:540px;">

    <!-- ── PROFILE CARD ── -->
    <div class="box mb-4 p-4">
      <div class="is-flex is-align-items-center" style="gap:16px;">

        <!-- Avatar -->
        <figure class="image is-64x64" style="flex-shrink:0;">
          {#if shop.avatar_url}
            <img class="is-rounded" src={shop.avatar_url} alt="avatar" style="object-fit:cover; width:64px; height:64px;">
          {:else}
            <div
              class="has-background-primary is-rounded is-flex is-align-items-center is-justify-content-center"
              style="width:64px; height:64px; border-radius:50%;"
            >
              <span class="icon has-text-white is-large"><i class="fas fa-user fa-lg"></i></span>
            </div>
          {/if}
        </figure>

        <!-- Info -->
        <div style="flex:1; min-width:0;">
          <div class="is-flex is-align-items-center is-flex-wrap-wrap" style="gap:6px;">
            <span class="has-text-weight-bold is-size-6">{shop.name}</span>
            {#if shop.verified}
              <span class="icon has-text-primary is-small"><i class="fas fa-circle-check"></i></span>
            {/if}
            <span class="tag is-primary is-small has-text-weight-bold" style="letter-spacing:.5px;">BUYER</span>
          </div>
          <p class="is-size-7 has-text-grey mt-1">
            <span class="mr-3"><strong>{shop.followers}</strong> Followers</span>
            <span><strong>{shop.following}</strong> Following</span>
          </p>
        </div>

        <!-- Actions -->
        
      </div>
    </div>

    <!-- ── STATS BAR ── -->
    <div class="box mb-4 p-0" style="overflow:hidden;">
      <div class="columns is-mobile m-0">
        {#each [
          { label: 'To Ship',   value: stats.toShip    },
          { label: 'Cancelled', value: stats.cancelled  },
          { label: 'Return',    value: stats.returned   },
          { label: 'Review',    value: stats.review     },
        ] as s, i}
          <div
            class="column has-text-centered py-4"
            style="border-right: {i < 3 ? '1px solid #f0f0f0' : 'none'}; cursor:pointer;"
          >
            <p class="has-text-weight-black is-size-4 has-text-dark">{s.value}</p>
            <p class="is-size-7 has-text-grey">{s.label}</p>
          </div>
        {/each}
      </div>
    </div>

    <!-- ── TABS ── -->
    <div class="tabs is-boxed is-fullwidth mb-0">
      <ul>
        <li class={activeTab === 'products' ? 'is-active' : ''}>
          <a onclick={() => activeTab = 'products'} role="button" tabindex="0"
             onkeydown={(e) => e.key === 'Enter' && (activeTab = 'products')}>
            <span class="icon is-small"><i class="fas fa-box-open"></i></span>
            <span>My Products</span>
          </a>
        </li>
        <li class={activeTab === 'orders' ? 'is-active' : ''}>
          <a onclick={() => activeTab = 'orders'} role="button" tabindex="0"
             onkeydown={(e) => e.key === 'Enter' && (activeTab = 'orders')}>
            <span class="icon is-small"><i class="fas fa-shopping-bag"></i></span>
            <span>My Orders</span>
          </a>
        </li>
      </ul>
    </div>

    <!-- ── MY PRODUCTS ── -->
    {#if activeTab === 'products'}
      <div class="box mt-0" style="border-radius:0 0 8px 8px; padding:0;">

        <!-- Add button row -->
        <div class="px-4 py-3 is-flex is-justify-content-flex-end"
             style="border-bottom:1px solid #f5f5f5;">
          <button class="button is-primary is-small is-rounded" onclick={() => goto('/addproduct')}>
            <span class="icon is-small"><i class="fas fa-plus"></i></span>
            <span>Add Product</span>
          </button>
        </div>

        {#if products.length === 0}
          <div class="has-text-centered py-6">
            <span class="icon is-large has-text-grey-light"><i class="fas fa-box-open fa-2x"></i></span>
            <p class="is-size-7 has-text-grey mt-2">ยังไม่มีสินค้า</p>
          </div>
        {:else}
          {#each products as p}
            <div
              class="is-flex is-align-items-center px-4 py-3"
              style="gap:14px; border-bottom:1px solid #f5f5f5; cursor:pointer;"
              onclick={() => goto(`/products/${p.id}`)}
              role="button" tabindex="0"
              onkeydown={(e) => e.key === 'Enter' && goto(`/products/${p.id}`)}
            >
              <!-- Thumb placeholder -->
              <div
                class="has-background-light is-flex is-align-items-center is-justify-content-center"
                style="width:48px; height:48px; border-radius:8px; flex-shrink:0;"
              >
                <span class="icon has-text-grey"><i class="fas fa-shirt"></i></span>
              </div>

              <div style="flex:1; min-width:0;">
                <p class="has-text-weight-semibold is-size-6 is-clipped">{p.pname}</p>
                <p class="is-size-7 has-text-grey">{p.brand}</p>
              </div>

              <div class="is-flex is-flex-direction-column is-align-items-flex-end" style="gap:5px;">
                <span class="has-text-weight-bold has-text-primary">฿{p.price}</span>
                <span class="tag is-small {statusColor(p.product_status)}">
                  {p.product_status === 'available' ? 'Active' : 'Sold'}
                </span>
              </div>
            </div>
          {/each}
        {/if}
      </div>

    <!-- ── MY ORDERS ── -->
    {:else}
      <div class="box mt-0" style="border-radius:0 0 8px 8px; padding:0;">
        {#if orders.length === 0}
          <div class="has-text-centered py-6">
            <span class="icon is-large has-text-grey-light"><i class="fas fa-shopping-bag fa-2x"></i></span>
            <p class="is-size-7 has-text-grey mt-2">ยังไม่มีคำสั่งซื้อ</p>
          </div>
        {:else}
          {#each orders as o}
            <div
              class="is-flex is-align-items-center px-4 py-3"
              style="gap:14px; border-bottom:1px solid #f5f5f5; cursor:pointer;"
              onclick={() => goto(`/orders/${o.id}`)}
              role="button" tabindex="0"
              onkeydown={(e) => e.key === 'Enter' && goto(`/orders/${o.id}`)}
            >
              <div
                class="has-background-primary-light is-flex is-align-items-center is-justify-content-center"
                style="width:44px; height:44px; border-radius:10px; flex-shrink:0;"
              >
                <span class="icon has-text-primary"><i class="fas fa-receipt"></i></span>
              </div>

              <div style="flex:1; min-width:0;">
                <p class="has-text-weight-semibold is-size-6 is-clipped">{o.product_name}</p>
                <p class="is-size-7 has-text-grey">#ORDER-{o.id}</p>
              </div>

              <div class="is-flex is-flex-direction-column is-align-items-flex-end" style="gap:5px;">
                <span class="has-text-weight-bold">฿{o.price}</span>
                <span class="tag is-small {orderStatusColor(o.status)}">
                  {orderStatusLabel(o.status)}
                </span>
              </div>
            </div>
          {/each}
        {/if}
      </div>
    {/if}

  </div>
</section>