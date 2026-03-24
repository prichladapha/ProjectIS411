<script>
  // รับ item (สินค้า), index (ตำแหน่ง), และฟังก์ชัน onRemove ผ่าน props
  let { item =$bindable(), index, onRemove } = $props();
</script>

<div class="columns is-mobile is-vcentered mb-3" style="position: relative;">
    <button 
      class="delete is-medium" 
      style="position: absolute; top: 0; right: 0; z-index: 10;"
      onclick={() => onRemove(index)}
    ></button>

    <div class="column is-narrow">
      <input type="checkbox" 
      bind:checked={item.selected} 
      class="checkbox">
    </div>

    <div class="column is-narrow">
      <figure class="image is-square" style="width: 80px;">
        <img src={item.img} alt={item.name} style="object-fit: cover; border-radius: 8px;" />
      </figure>
    </div>

    <div class="column">
      <p class="has-text-weight-bold">{item.name}</p>
      <p class="is-size-7 has-text-grey">{item.shop}</p>
      <p class="has-text-primary">฿{item.price.toLocaleString()}</p>
    </div>
</div>
<hr />