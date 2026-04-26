<script>
  import { currentUser } from '$lib/shared';
  import { goto } from '$app/navigation';

  let { data } = $props();

  // State สำหรับ Svelte 5
  let staticComments = $state(data.post.staticComments || []);
  let commentText = $state("");
  let isTyping = $state(false);
  let dropdownOpen = $state(false);
  let sortMode = $state('Recent');

  let post = $derived(data.post);

  async function postComment() {
    if (!$currentUser) {
      goto('/signin');
      return;
    }
    if (commentText.trim() === "") return;

    // URL ต้อตรงกับ Backend (@app.post("/posts/{post_id}/comments"))
    const res = await fetch(`http://127.0.0.1:8000/posts/${post.id}/comments`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        text: commentText.trim(),
        customer_id: $currentUser.customer_id
        // ไม่ต้องส่ง post_id ใน Body แล้ว เพราะเราส่งไปทาง URL แทนตาม Backend ใหม่
      })
    });

    if (res.ok) {
      const newCommentFromServer = await res.json();
      
      // เอาข้อมูลที่ Backend return กลับมา 
      staticComments = [...staticComments, {
        name: newCommentFromServer.name,
        avatar: newCommentFromServer.avatar,
        text: newCommentFromServer.text,
        time: newCommentFromServer.time
      }];
      
      commentText = "";
      isTyping = false;
    }
  }
</script>

<section class="section pt-3">
  <div class="post-detail-card">

    <div class="is-flex is-align-items-center mb-2">
      <figure class="image is-32x32 mr-2">
        <img class="is-rounded" src={post.avatar} alt="avatar"
          style="object-fit:cover; width:32px; height:32px;">
      </figure>
      <div>
        <p style="font-size:0.85rem; font-weight:600; margin:0;">{post.name}</p>
        <p style="font-size:0.75rem; color:#888; margin:0;">@{post.username}</p>
      </div>
    </div>

    <p style="font-size:0.85rem; margin-bottom:10px;">{post.content}</p>

    {#if post.image}
      <div style="display:flex; justify-content:center; overflow-x:auto; gap:8px; scroll-snap-type:x mandatory; -webkit-overflow-scrolling:touch;">
        <img src={post.image} alt="post"
          style="aspect-ratio:4/5; width:260px; border-radius:8px; flex-shrink:0; scroll-snap-align:start; object-fit:cover;" />
      </div>
    {/if}

    <div class="is-flex mt-3" style="justify-content:space-between;">
      <span class="icon-text" style="font-size:0.8rem;">
        <span class="icon is-small has-text-danger"><i class="fas fa-heart"></i></span>
        <span>{post.likes ?? 0}</span>
      </span>
      <span class="icon-text" style="font-size:0.8rem;">
        <span class="icon is-small has-text-info"><i class="fas fa-comment"></i></span>
        <span>{staticComments.length}</span>
      </span>
      <span class="icon-text" style="font-size:0.8rem;">
        <span class="icon is-small has-text-success"><i class="fas fa-retweet"></i></span>
        <span>{post.reposts ?? 0}</span>
      </span>
      <span class="icon-text" style="font-size:0.8rem;">
        <span class="icon is-small has-text-grey"><i class="fas fa-paper-plane"></i></span>
        <span>{post.shares ?? 0}</span>
      </span>
    </div>

    <div style="border-top: 1px solid #eaeaea; border-bottom: 1px solid #eaeaea; padding: 8px 0; margin-top:12px;">
      <div style="position:relative; display:inline-block;">
        <button class="button is-white is-small" onclick={() => dropdownOpen = !dropdownOpen}>
          <span style="font-size:0.8rem;">{sortMode}</span>
          <span class="icon is-small"><i class="fas fa-chevron-down"></i></span>
        </button>

        {#if dropdownOpen}
          <div style="position:absolute; background:white; border:1px solid #eaeaea; border-radius:6px; z-index:10; min-width:120px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
            {#each ['Recent', 'Popular'] as mode}
              <a class="dropdown-item" style="font-size:0.8rem; display:block; padding:8px 16px; cursor:pointer;"
                onclick={() => { sortMode = mode; dropdownOpen = false; }}>
                {mode}
              </a>
            {/each}
          </div>
        {/if}
      </div>
    </div>

    <div class="mt-4">
      {#each staticComments as c}
        <div class="is-flex mb-4" style="gap:10px;">
          <figure class="image is-32x32" style="flex-shrink:0;">
            <img class="is-rounded" src={c.avatar} alt="avatar"
              style="object-fit:cover; width:32px; height:32px;" />
          </figure>
          <div style="flex:1;">
            <p style="font-size:0.8rem; font-weight:600; margin:0;">{c.name}</p>
            <p style="font-size:0.8rem; margin:0; color: #333;">{c.text}</p>
            <p style="font-size:0.72rem; color:#aaa; margin-top:2px;">{c.time || 'Just now'} · <a>Like</a> · <a>Reply</a></p>
          </div>
        </div>
      {/each}

      <div class="is-flex mt-4" style="gap:10px;">
        <figure class="image is-32x32" style="flex-shrink:0;">
          <img class="is-rounded" src={$currentUser?.avatar || 'https://placehold.co/100x100'} 
               alt="me" style="object-fit:cover; width:32px; height:32px;" />
        </figure>

        <div style="flex:1;">
          {#if isTyping}
            <p style="font-size:0.72rem; color:#aaa; margin-bottom:4px;">
              Reply to <strong>{post.username}</strong>
            </p>
          {/if}

          <textarea class="textarea" style="font-size:0.85rem; min-height: 2.5em; border-radius: 8px;"
            bind:value={commentText}
            placeholder="Add a comment..."
            onfocus={() => isTyping = true}>
          </textarea>

          {#if isTyping || commentText}
            <div class="is-flex is-align-items-center is-justify-content-space-between mt-2">
              <div class="is-flex" style="gap:12px; color: #666;">
                <span class="icon is-small" style="cursor:pointer;"><i class="fas fa-image"></i></span>
                <span style="cursor:pointer; font-size:0.7rem; font-weight:bold; border:1px solid #ccc; border-radius:4px; padding:0 4px;">GIF</span>
              </div>
              <button class="button is-primary is-small is-rounded" onclick={postComment}>
                Post
              </button>
            </div>
          {/if}
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
    border-radius: 12px;
    padding: 16px;
    border: 1px solid #efefef;
  }
  .dropdown-item:hover {
    background-color: #f5f5f5;
  }
</style>