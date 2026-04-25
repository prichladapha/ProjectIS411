<script>
    import { cartStore, checkout } from '$lib/cart.svelte.js';
</script>

<section class="section">
    <div class="container">
        <h1 class="title is-3 has-text-centered mb-6">Checkout</h1>

        <div class="columns is-centered">
            <div class="column is-7">
                <div class="box">
                    <h2 class="subtitle is-5">📦 Order Details</h2>
                    <hr>
                    <table class="table is-fullwidth">
                        <thead>
                            <tr>
                                <th>Product</th>
                                <th class="has-text-centered">Qty</th>
                                <th class="has-text-right">Price</th>
                            </tr>
                        </thead>
                        <tbody>
                            {#each cartStore.items as item}
                                <tr>
                                    <td>
                                        <strong>{item.name}</strong><br>
                                        <span class="is-size-7 has-text-grey">{item.shop}</span>
                                    </td>
                                    <td class="has-text-centered">{item.qty || 1}</td>
                                    <td class="has-text-right">{item.price.toLocaleString()} ฿</td>
                                </tr>
                            {/each}
                        </tbody>
                    </table>
                </div>
            </div>

            <div class="column is-4">
                <div class="box has-background-white-ter">
                    <h2 class="subtitle is-5">💰 Summary</h2>
                    <hr>
                    <div class="is-flex is-justify-content-space-between mb-3">
                        <span>Subtotal</span>
                        <span>{cartStore.total.toLocaleString()} ฿</span>
                    </div>
                    <div class="is-flex is-justify-content-space-between mb-3">
                        <span>Shipping Fee</span>
                        <span>50 ฿</span>
                    </div>
                    <hr>
                    <div class="is-flex is-justify-content-space-between mb-5">
                        <span class="title is-5">Total</span>
                        <span class="title is-5 has-text-danger">
                            {(cartStore.total + 50).toLocaleString()} ฿
                        </span>
                    </div>

                    <button 
                        class="button is-primary is-fullwidth is-large is-rounded"
                        onclick={checkout}
                        disabled={cartStore.count === 0}
                    >
                        <strong>Confirm and Pay</strong>
                    </button>
                    
                    <a href="/cart" class="button is-ghost is-fullwidth mt-2">Edit Cart</a>
                </div>
            </div>
        </div>
    </div>
</section>