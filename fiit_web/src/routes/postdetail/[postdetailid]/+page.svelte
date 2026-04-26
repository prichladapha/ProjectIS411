<script>
  import { currentUser } from '$lib/shared';
  import { enhance } from '$app/forms';

  // 1. รับข้อมูล: 'data' (จาก load) และ 'form' (จาก action เมื่อกดส่งคอมเมนต์)
  let { data, form } = $props();

  // 2. Local State: จัดการ UI เล็กๆ น้อยๆ เช่น การเปิด Dropdown หรือสถานะการพิมพ์
  let commentText = $state("");
  let isTyping = $state(false);
  let dropdownOpen = $state(false);
  let sortMode = $state('Recent');

  // 3. Derived State: ใช้ $derived เพื่อคำนวณค่าใหม่ทุกครั้งที่ data เปลี่ยน 
  let post = $derived(data.post || {});
  let staticComments = $derived(data.post?.staticComments || []);

  // 4. Side Effect: เมื่อส่งคอมเมนต์สำเร็จ ให้เคลียร์ช่องกรอกข้อมูล
  $effect(() => {
    if (form?.success) {
      commentText = ""; 
      isTyping = false;
    }
  });
</script>

<section class="section pt-3">
  <div class="post-detail-card">
    <div class="is-flex is-align-items-center mb-3">
      <figure class="image is-40x40 mr-3">
        <img src={post.avatar} alt="avatar"
          style="object-fit:cover; width:40px; height:40px; border-radius: 50%;">
      </figure>
      <div style="line-height: 1.2;">
        <p class="has-text-weight-bold" style="font-size:0.95rem;">{post.name}</p>
        <p style="font-size:0.8rem; color:#888;">@{post.username}</p>
      </div>
    </div>

    <p class="mb-3" style="font-size:0.95rem; line-height: 1.5;">{post.content}</p>

    {#if post.image}
      <div class="mb-3" style="border-radius: 12px; overflow: hidden; border: 1px solid #efefef;">
        <img src={post.image} alt="post" style="width:100%; max-height:400px; object-fit:cover;" />
      </div>
    {/if}

    <div class="is-flex mt-3 pb-3" style="justify-content:space-between; border-bottom: 1px solid #f5f5f5;">
      <span class="icon-text has-text-grey" style="font-size:0.8rem;">
        <span class="icon is-small"><i class="far fa-heart"></i></span>
        <span>{post.likes ?? 0}</span>
      </span>
      <span class="icon-text has-text-grey" style="font-size:0.8rem;">
        <span class="icon is-small"><i class="far fa-comment"></i></span>
        <span>{staticComments.length}</span>
      </span>
      <span class="icon-text has-text-grey" style="font-size:0.8rem;">
        <span class="icon is-small"><i class="fas fa-retweet"></i></span>
        <span>{post.reposts ?? 0}</span>
      </span>
      <span class="icon-text has-text-grey" style="font-size:0.8rem;">
        <span class="icon is-small"><i class="far fa-paper-plane"></i></span>
        <span>{post.shares ?? 0}</span>
      </span>
    </div>

    <div class="py-2 mb-4">
      <div style="position:relative; display:inline-block;">
        <button class="button is-white is-small px-0" onclick={() => dropdownOpen = !dropdownOpen}>
          <span class="has-text-weight-semibold" style="font-size:0.8rem;">{sortMode}</span>
          <span class="icon is-small"><i class="fas fa-chevron-down" style="font-size: 0.6rem;"></i></span>
        </button>

        {#if dropdownOpen}
          <div class="dropdown-content-custom">
            {#each ['Recent', 'Popular'] as mode}
              <button class="dropdown-item-btn" onclick={() => { sortMode = mode; dropdownOpen = false; }}>
                {mode}
              </button>
            {/each}
          </div>
        {/if}
      </div>
    </div>

    <div class="comments-container">
      {#each staticComments as c}
        <div class="is-flex mb-4" style="gap:12px;">
          <figure class="image is-32x32" style="flex-shrink:0;">
            <img src={c.avatar} alt="avatar"
              style="object-fit:cover; width:32px; height:32px; border-radius: 50%;" />
          </figure>
          <div style="flex:1;">
            <div class="comment-bubble">
                <p class="has-text-weight-bold" style="font-size:0.8rem; margin-bottom: 2px;">{c.name}</p>
                <p style="font-size:0.85rem; color: #333;">{c.text}</p>
            </div>
            <p style="font-size:0.72rem; color:#aaa; margin-top:4px; margin-left: 4px;">
                {c.time || 'Just now'} · <a class="has-text-grey">Like</a> · <a class="has-text-grey">Reply</a>
            </p>
          </div>
        </div>
      {/each}

      <div class="is-flex mt-5" style="gap:12px;">
        <figure class="image is-32x32" style="flex-shrink:0;">
          <img src={$currentUser?.avatar || 'https://placehold.co/100x100'} 
               alt="me" style="object-fit:cover; width:32px; height:32px; border-radius: 50%;" />
        </figure>

        <div style="flex:1;">
          <form method="POST" use:enhance>
            <input type="hidden" name="customer_id" value={$currentUser?.customer_id} />

            {#if form?.error}
              <p class="has-text-danger is-size-7 mb-2">{form.error}</p>
            {/if}

            {#if isTyping}
              <p style="font-size:0.72rem; color:#aaa; margin-bottom:4px;">
                Reply to <strong>{post.username}</strong>
              </p>
            {/if}

            <textarea class="textarea comment-textarea" 
              name="commentText"
              bind:value={commentText}
              placeholder="Add a comment..."
              onfocus={() => isTyping = true}
              rows={isTyping ? 3 : 1}>
            </textarea>

            {#if isTyping || commentText}
              <div class="is-flex is-align-items-center is-justify-content-space-between mt-2">
                <div class="is-flex" style="gap:15px; color: #adb5bd;">
                  <span class="is-clickable action-icon-small"><i class="far fa-image"></i></span>
                  <span class="is-clickable action-icon-small"><i class="far fa-smile"></i></span>
                </div>
                <button type="submit" 
                        class="button is-primary is-small is-rounded px-4 has-text-weight-bold"
                        disabled={!commentText.trim()}>
                  Post
                </button>
              </div>
            {/if}
          </form>
        </div>
      </div>
    </div>
  </div>
</section>

<style>
  .post-detail-card {
    max-width: 520px;
    width: 100%;
    margin: 0 auto;
    background: white;
    padding: 16px;
  }

  .comment-bubble {
    background-color: #f0f2f5;
    padding: 8px 12px;
    border-radius: 18px;
    display: inline-block;
    max-width: 100%;
  }

  .comment-textarea {
    font-size: 0.9rem;
    border-radius: 20px;
    background-color: #f0f2f5;
    border: none;
    box-shadow: none;
    resize: none;
    transition: all 0.2s;
  }
  .comment-textarea:focus {
    background-color: #fff;
    border: 1px solid #eee;
  }

  .dropdown-content-custom {
    position:absolute; 
    background:white; 
    border:1px solid #efefef; 
    border-radius:12px; 
    z-index:10; 
    min-width:120px; 
    box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    padding: 4px;
  }

  .dropdown-item-btn {
    width: 100%;
    text-align: left;
    background: none;
    border: none;
    padding: 8px 12px;
    font-size: 0.8rem;
    cursor: pointer;
    border-radius: 8px;
  }
  .dropdown-item-btn:hover { background-color: #f5f5f5; }

  .action-icon-small { font-size: 1rem; transition: color 0.2s; }
  .action-icon-small:hover { color: #00d1b2; }
</style>

