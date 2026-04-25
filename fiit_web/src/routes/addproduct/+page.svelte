<script>
  import { goto } from '$app/navigation';

  let { data } = $props();

  let pname = $state('');
  let price = $state('');
  let brand = $state('');
  let description = $state('');
  let categoryID = $state('');
  let seller_id = $state(data?.user?.seller_id ?? '');
  let tags = $state('');
  let product_status = $state('available');
  let image_url = $state('');

  let mainPreview = $state('');
  let frontPreview = $state('');
  let backPreview = $state('');
  let checkFlaw = $state(false);
  let flawDetail = $state('');
  let condition = $state('');
  let loading = $state(false);
  let errorMsg = $state('');

  function handleMainPhoto(e) {
    const file = e.target.files[0];
    if (!file) return;
    mainPreview = URL.createObjectURL(file);
    image_url = mainPreview;
  }

  function handleFrontPhoto(e) {
    const file = e.target.files[0];
    if (!file) return;
    frontPreview = URL.createObjectURL(file);
  }

  function handleBackPhoto(e) {
    const file = e.target.files[0];
    if (!file) return;
    backPreview = URL.createObjectURL(file);
  }

  async function handleSave() {
    errorMsg = '';
    if (!pname || !price || !brand || !description || !categoryID || !seller_id || !tags || !condition) {
      errorMsg = 'กรุณากรอกข้อมูลที่จำเป็นให้ครบถ้วน';
      return;
    }
    loading = true;
    try {
      const body = {
        pname,
        price: parseFloat(price),
        brand,
        description,
        categoryID: parseInt(categoryID),
        seller_id: parseInt(seller_id),
        tags,
        product_status,
        image_url: image_url || null
      };
      const res = await fetch('http://localhost:8000/products/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body)
      });
      if (!res.ok) {
        const err = await res.json();
        errorMsg = err.detail || 'เกิดข้อผิดพลาด กรุณาลองใหม่';
        return;
      }
      alert('เพิ่มสินค้าสำเร็จ!');
      goto('/');
    } catch (e) {
      errorMsg = 'ไม่สามารถเชื่อมต่อ server ได้';
    } finally {
      loading = false;
    }
  }
</script>

<!-- Header -->
<div class="has-background-primary px-4 py-3 is-flex is-align-items-center" style="gap:12px; position:sticky; top:0; z-index:10;">
  <button class="delete is-medium" style="background:rgba(255,255,255,0.3);" onclick={() => goto('/myshop')}></button>
  <span class="has-text-white has-text-weight-bold is-size-6" style="letter-spacing:1px;">ADD PRODUCT</span>
</div>

<section class="section pt-4 pb-6">
  <div class="container" style="max-width:480px;">

    <!-- รูปหลัก -->
    <div class="has-text-centered mb-5">
      <label class="photo-circle">
        {#if mainPreview}
          <img src={mainPreview} alt="preview" class="photo-preview-circle">
        {:else}
          <span class="is-size-3 has-text-grey-light">+</span>
        {/if}
        <input type="file" accept="image/*" onchange={handleMainPhoto} style="display:none;">
      </label>
      <p class="is-size-7 has-text-grey mt-3">อัพโหลดรูปหลัก</p>
    </div>

    {#if errorMsg}
      <div class="notification is-danger is-light mb-4">{errorMsg}</div>
    {/if}

    <div class="field">
      <label class="label is-small">PRODUCT NAME <span class="has-text-danger">*</span></label>
      <div class="control">
        <input class="input" type="text" placeholder="Enter Product Name" bind:value={pname}>
      </div>
    </div>

    <div class="field">
      <label class="label is-small">PRODUCT DESCRIPTION <span class="has-text-danger">*</span></label>
      <div class="control">
        <textarea class="textarea" rows="3" placeholder="Enter Product Description" bind:value={description}></textarea>
      </div>
    </div>

    <div class="field">
      <label class="label is-small">BRAND <span class="has-text-danger">*</span></label>
      <div class="control">
        <input class="input" type="text" placeholder="Enter Brand" bind:value={brand}>
      </div>
    </div>

    <div class="columns is-mobile">
      <div class="column">
        <div class="field">
          <label class="label is-small">PRICE <span class="has-text-danger">*</span></label>
          <div class="control">
            <input class="input" type="number" placeholder="0.00" bind:value={price}>
          </div>
        </div>
      </div>
      <div class="column">
        <div class="field">
          <label class="label is-small">CATEGORY <span class="has-text-danger">*</span></label>
          <div class="control">
            <div class="select is-fullwidth">
              <select bind:value={categoryID}>
                <option value="">Choose...</option>
                {#each data?.categories ?? [] as cat}
                  <option value={cat.category_id}>{cat.category_name}</option>
                {/each}
              </select>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="field">
      <label class="label is-small">TAGS <span class="has-text-danger">*</span></label>
      <div class="control">
        <input class="input" type="text" placeholder="เช่น เสื้อ, วินเทจ, Uniqlo" bind:value={tags}>
      </div>
    </div>

    <div class="field">
      <label class="label is-small">CHECK LIST</label>
      <div class="is-flex" style="gap:16px; flex-wrap:wrap;">
        <label class="checkbox is-size-7"><input type="checkbox"> Size Information</label>
        <label class="checkbox is-size-7"><input type="checkbox"> No Flaw</label>
        <label class="checkbox is-size-7"><input type="checkbox" bind:checked={checkFlaw}> Flaw</label>
      </div>
      {#if checkFlaw}
        <div class="control mt-2">
          <input class="input is-small" type="text" placeholder="Enter Flaw Detail" bind:value={flawDetail}>
        </div>
      {/if}
    </div>

    <div class="field">
      <label class="label is-small">REQUIREMENT PHOTO</label>
      <div class="columns is-mobile">
        <div class="column">
          <label class="photo-box">
            {#if frontPreview}
              <img src={frontPreview} alt="front" class="photo-preview">
            {:else}
              <span class="is-size-7 has-text-grey-light">Front View *</span>
            {/if}
            <input type="file" accept="image/*" onchange={handleFrontPhoto} style="display:none;">
          </label>
        </div>
        <div class="column">
          <label class="photo-box">
            {#if backPreview}
              <img src={backPreview} alt="back" class="photo-preview">
            {:else}
              <span class="is-size-7 has-text-grey-light">Back View *</span>
            {/if}
            <input type="file" accept="image/*" onchange={handleBackPhoto} style="display:none;">
          </label>
        </div>
      </div>
    </div>

    <div class="field">
      <label class="label is-small">ITEM CONDITION <span class="has-text-danger">*</span></label>
      <div class="is-flex" style="flex-direction:column; gap:8px;">
        {#each ['New with tag', 'Like new', 'Good', 'Fair'] as cond}
          <label class="radio is-size-7">
            <input type="radio" name="condition" value={cond} bind:group={condition}> {cond}
          </label>
        {/each}
      </div>
    </div>

    <div class="field mt-5">
      <div class="control">
        <button
          class="button is-primary is-fullwidth is-rounded has-text-weight-bold"
          onclick={handleSave}
          disabled={loading}>
          {loading ? 'กำลังบันทึก...' : 'SAVE'}
        </button>
      </div>
    </div>

  </div>
</section>

<style>
  .photo-circle {
    width: 90px;
    height: 90px;
    border-radius: 50%;
    border: 2px dashed #ccc;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    overflow: hidden;
    background: #f5f5f5;
  }

  .photo-preview-circle {
    width: 100%;
    height: 100%;
    object-fit: cover;
  }

  .photo-box {
    border: 1.5px dashed #ccc;
    border-radius: 8px;
    height: 100px;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    overflow: hidden;
    background: #fafafa;
    width: 100%;
  }

  .photo-preview {
    width: 100%;
    height: 100%;
    object-fit: cover;
  }
</style>