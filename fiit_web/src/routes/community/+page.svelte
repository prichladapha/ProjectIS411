<script>
  import { goto } from '$app/navigation';
  import { currentUser } from '$lib/shared';
  import { enhance } from '$app/forms';

  // 1. รับข้อมูลจาก Server: 'data' มาจาก PageServerLoad และ 'form' มาจาก Actions 
  let { data, form } = $props(); 

  // 2. Local State: ใช้ $state สำหรับตัวแปรที่ต้องการให้หน้าจออัปเดตอัตโนมัติ 
  let isModalOpen = $state(false);
  let newPostContent = $state("");
  let imagePreview = $state(null);

  // 3. Side Effects: ใช้ $effect จัดการเหตุการณ์หลังจาก Server ตอบกลับมา (เช่น ปิด Modal เมื่อโพสต์สำเร็จ)
  $effect(() => {
    if (form?.success) {
      isModalOpen = false;
      newPostContent = "";
      imagePreview = null;
      // หมายเหตุ: data.posts จะอัปเดตให้อัตโนมัติเพราะใช้ use:enhance
    }
  });
</script>

<section class="section pt-3">
  <div class="mt-4">
    {#each data.posts as post (post.id)}
      <div class="card mb-3 post-card" onclick={() => goto(`/postdetail/${post.id}`)}>
        <div class="card-content">
          <div class="is-flex is-align-items-center mb-2">
            <figure class="image is-32x32 mr-2">
              <img class="is-rounded" src={post.avatar} alt="avatar" style="object-fit:cover; width:32px; height:32px; border-radius: 50%;">
            </figure>
            <div>
              <p style="font-size:0.85rem; font-weight:600; margin:0;">{post.name}</p>
              <p style="font-size:0.75rem; color:#888; margin:0;">@{post.username}</p>
            </div>
          </div>

          <p style="font-size:0.85rem; margin-bottom:10px;">{post.content}</p>

          {#if post.image}
            <div style="display:flex; justify-content:center; overflow-x:auto; gap:8px;">
              <img src={post.image} alt="post" style="aspect-ratio:4/5; width:260px; border-radius:8px; object-fit:cover;" />
            </div>
          {/if}

          <div class="is-flex mt-2" style="justify-content:space-between;">
            <span class="icon-text hover-heart"><span class="icon is-small"><i class="far fa-heart"></i></span><span>{post.likes}</span></span>
            <span class="icon-text hover-comment"><span class="icon is-small"><i class="far fa-comment"></i></span><span>{post.comments}</span></span>
            <span class="icon-text hover-retweet"><span class="icon is-small"><i class="fas fa-retweet"></i></span><span>{post.reposts}</span></span>
            <span class="icon-text hover-share"><span class="icon is-small"><i class="far fa-paper-plane"></i></span><span>{post.shares}</span></span>
          </div>
        </div>
      </div>
    {/each}
  </div>

  <button class="button is-primary is-rounded shadow-fab" onclick={() => isModalOpen = true}>
    <span class="icon"><i class="fas fa-plus"></i></span>
  </button>
</section>

<div class="modal {isModalOpen ? 'is-active' : ''}">
  <div class="modal-background" onclick={() => isModalOpen = false}></div>
  <div class="modal-card custom-modal-card">
    
    <form method="POST" action="?/createPost" use:enhance>
      
      <header class="modal-card-head is-borderless has-background-white pt-5">
        <button type="button" class="delete" aria-label="close" onclick={() => isModalOpen = false}></button>
        <p class="modal-card-title has-text-centered is-size-6 has-text-weight-bold">New Post</p>
        <div style="width: 32px;"></div>
      </header>

      <section class="modal-card-body pb-0">
        {#if form?.error}
          <div class="notification is-danger is-light p-2 mb-3" style="font-size: 0.8rem;">
            {form.error}
          </div>
        {/if}

        <div class="is-flex" style="gap: 15px;">
          <div class="is-flex is-flex-direction-column is-align-items-center">
            <figure class="image is-48x48">
              <img src={$currentUser?.avatar || 'https://placehold.co/100x100'} alt="me" 
                style="object-fit: cover; width: 48px; height: 48px; border-radius: 50%;">
            </figure>
            <div class="thread-line"></div>
          </div>

          <div style="flex: 1;">
            <p class="has-text-weight-bold is-size-6 mb-1">{ $currentUser?.username || 'user' }</p>
            
            <input type="hidden" name="customer_id" value={$currentUser?.customer_id} />
            
            <textarea 
              name="content"
              class="textarea custom-textarea" 
              placeholder="What's on your mind?" 
              bind:value={newPostContent}
              rows="2"></textarea>

            <div class="is-flex mt-2 mb-4" style="gap: 20px; color: #ccc; font-size: 1.2rem;">
              <span class="is-clickable hover-grey"><i class="far fa-image"></i></span>
              <span class="is-clickable hover-grey"><i class="far fa-smile"></i></span>
            </div>
          </div>
        </div>
      </section>

      <footer class="modal-card-foot is-borderless has-background-white is-justify-content-space-between px-5 pb-5">
        <div class="is-size-7 has-text-grey">Anyone can reply</div>
        <button type="submit" 
          class="button is-rounded px-6" 
          class:is-primary={newPostContent.trim()} 
          disabled={!newPostContent.trim()}
          style="font-weight: bold; height: 40px; border: 1px solid #f0f0f0;">
          Post
        </button>
      </footer>
    </form>
  </div>
</div>

<style>
  /* จัดการ Layout ของการ์ดโพสต์ */
  .post-card {
    max-width: 520px;
    width: 100%;
    margin: 0 auto 12px auto;
    cursor: pointer;
    border-radius: 12px;
    border: 1px solid #efefef;
    transition: background-color 0.2s ease;
  }
  .post-card:hover { background-color: #f9f9f9; }

  /* ปุ่ม FAB ลอยตัว */
  .shadow-fab {
    position: fixed;
    bottom: 32px;
    right: 32px;
    width: 56px;
    height: 56px;
    border-radius: 50%;
    font-size: 24px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
    z-index: 50;
    border: none;
  }

  /* ตกแต่ง Modal ให้ดูทันสมัย */
  .custom-modal-card {
    max-width: 600px;
    width: 95%;
    border-radius: 20px;
    overflow: hidden;
    box-shadow: 0 10px 40px rgba(0, 0, 0, 0.1);
  }

  .is-borderless { border: none !important; }

  /* ช่องพิมพ์ที่ไม่มีขอบ (แบบ Social Media) */
  .custom-textarea {
    border: none !important;
    box-shadow: none !important;
    padding: 5px 0 !important;
    font-size: 1.1rem;
    resize: none;
    background: transparent;
    min-height: 40px;
    color: #333;
  }

  /* เส้นแนวตั้งเชื่อมโยงรูปโปรไฟล์ (สไตล์ Threads) */
  .thread-line {
    width: 2px;
    background-color: #f0f0f0;
    flex-grow: 1;
    margin: 10px 0;
    min-height: 40px;
  }

  .hover-grey:hover { color: #888; }

  /* เอฟเฟกต์สีเมื่อนำเมาส์ไปชี้ไอคอน Stats */
  .icon-text {
    cursor: pointer;
    transition: color 0.2s;
    color: #65676b;
    font-size: 0.8rem;
  }
  .hover-heart:hover { color: #f14668 !important; }
  .hover-comment:hover { color: #3e8ed0 !important; }
  .hover-retweet:hover { color: #48c78e !important; }
  .hover-share:hover { color: #485fc7 !important; }
</style>

