<script>
  import { onMount } from 'svelte';
  import { currentUser } from '$lib/shared';
  import { goto } from '$app/navigation';

  let { data } = $props();
  let orders = $state([]);
  let loading = $state(true);

  onMount(async () => {
    if (!$currentUser) { loading = false; return; }

    const res = await fetch(`http://localhost:8000/orders/customer/${$currentUser.customer_id}`);
    if (!res.ok) { loading = false; return; }
    const orderList = await res.json();

    // ดึง items ของแต่ละ order
    orders = await Promise.all(orderList.map(async (order) => {
      const itemRes = await fetch(`http://localhost:8000/order_items/${order.order_id}`);
      const detail = itemRes.ok ? await itemRes.json() : { items: [] };
      return { ...order, items: detail.items };
    }));

    loading = false;
  });
</script>

<!-- Header -->
<div
  class="has-background-primary px-4 py-3 is-flex is-align-items-center is-justify-content-space-between"
  style="position:sticky; top:0; z-index:10;"
>
  <div class="is-flex is-align-items-center" style="gap:12px;">
  <button
    class="button is-ghost px-1"
    style="color:white;"
    onclick={() => goto('/profile')}
  >
    <span class="icon"><i class="fas fa-arrow-left"></i></span>
  </button>
  <span class="has-text-white has-text-weight-bold is-size-6" style="letter-spacing:1px;">
    MY ORDERS
  </span>
</div>
</div>


<section class="section">
  <div class="container">
    <div class="columns is-centered">
      <div class="column is-8-desktop">

        {#if loading}
          <div class="has-text-centered py-6">
            <p class="has-text-grey">Loading...</p>
          </div>

        {:else if orders.length === 0}
          <div class="box has-text-centered py-6">
            <p class="is-size-5 has-text-grey mb-3">You don’t have any order history yet.</p>
            <a href="/" class="button is-primary">Start shopping</a>
          </div>

        {:else}
          {#each orders as order}
            <div class="box mb-4">

              <!-- Order Header -->
              <div class="is-flex is-justify-content-space-between is-align-items-center mb-3">
                <h3 class="title is-5 mb-0">Order #{order.order_id}</h3>
                <span class="tag is-medium is-light
                  {order.order_status === 'pending' ? 'is-warning' :
                   order.order_status === 'paid' ? 'is-success' :
                   order.order_status === 'cancelled' ? 'is-danger' : 'is-info'}">
                  {order.order_status}
                </span>
              </div>

              <!-- Order Items -->
              {#each order.items ?? [] as item}
                <div class="is-flex is-justify-content-space-between is-align-items-center py-2"
                     style="border-bottom: 1px solid #f5f5f5;">
                  <div>
                    <p class="has-text-weight-semibold">{item.product_name}</p>
                    <p class="is-size-7 has-text-grey">{item.brand}</p>
                  </div>
                  <span class="has-text-weight-bold has-text-primary">
                    ฿{item.price.toLocaleString()}
                  </span>
                </div>
              {/each}

              <!-- Order Footer -->
              <div class="is-flex is-justify-content-space-between mt-3">
                <span class="has-text-grey is-size-7">
                  วันที่สั่ง: {order.created_at?.slice(0, 10) ?? '-'}
                </span>
                <span class="has-text-weight-bold">
                  รวม ฿{order.grand_total?.toLocaleString()}
                </span>
              </div>

            </div>
          {/each}
        {/if}

      </div>
    </div>
  </div>
</section>