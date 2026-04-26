<script>
  // รับ item (สินค้า), index (ตำแหน่ง), และฟังก์ชัน onRemove ผ่าน props
  let { item = $bindable(), index, onRemove } = $props();
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
      <figure class="image is-4by3" style="width: 100px;"> <img 
          src={item.img || 'https://placehold.co/400x300?text=No+Image'} 
          alt={item.name} 
          style="object-fit: contain; border-radius: 8px; background-color: #f5f5f5;" 
        />
      </figure>
    </div>

    <div class="column">
      <p class="has-text-weight-bold is-size-6">{item.name}</p>
      
      <p class="is-size-7 has-text-grey mb-1" style="display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden;">
        {item.description || item.detail || 'ไม่มีรายละเอียด'}
      </p>
      
      <p class="has-text-primary has-text-weight-semibold">
        ฿{item.price ? item.price.toLocaleString() : '0'}
      </p>
    </div>
</div>
<hr />