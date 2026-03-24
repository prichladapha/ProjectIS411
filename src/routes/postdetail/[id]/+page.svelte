
<!-- หน้า Post Detail — แสดงโพสที่กดมาจากฟีด พร้อมคอมเมนต์ -->
<script>
  let { data } = $props()

  import { currentUser } from '$lib/shared';
  import { goto } from '$app/navigation';

  let post = data.post;

  // กดpost commentเม้นแล้วขึ้นเม้นใหม่
  let commentText = "";
  let comments = [];
  
  // ถ้ายังไม่ได้ signin ให้เด้งไปหน้า signin
  function postComment() {
    if (!$currentUser) {
      goto('/signin');
      return;
    }
    if (commentText.trim() === "") return;
    comments = [...comments, commentText.trim()];
    commentText = "";
  }
</script>

<!-- ถ้าหาโพสไม่เจอ -->
{#if !post}
  <p>ไม่พบโพสนี้</p>

{:else}

<section class="section pt-3">
  <div class="card" style="max-width:1400px; margin:auto;">
    <div class="card-content">

      <!-- ข้อมูลคนโพส: รูป ชื่อ username -->
      <div class="media">
        <div class="media-left">
          <figure class="image is-48x48">
            <img class="is-rounded" src={post.avatar}
              style="object-fit: cover; width:100%; height:100%;">
          </figure>
        </div>
        <div class="media-content">
          <p class="title is-4">{post.name}</p>
          <p class="subtitle is-6">{post.username}</p>
        </div>
      </div>

      <!-- เนื้อหาโพส -->
      <div class="content">{post.content}</div>

      <!-- รูปภาพในโพส -->
      <div class="card-image">
        <figure>
          <img src={post.image} alt="post image"
            style="width:100%; height:auto; max-height:500px; object-fit:contain; border-radius:8px;" />
        </figure>
      </div>

      <!-- ไอคอน เมนท์ แชร์-->
      <div class="is-flex is-align-items-center mt-3" style="gap: 24px;">
        <span class="icon-text">
          <span class="icon"><i class="fas fa-heart"></i></span>
          <span>{post.likes ?? 0}</span>
        </span>
        <span class="icon-text">
          <span class="icon"><i class="fas fa-comment"></i></span>
          <span>{post.staticComments.length + comments.length}</span>
        </span>
        <span class="icon-text">
          <span class="icon"><i class="fas fa-retweet"></i></span>
          <span>{post.reposts ?? 0}</span>
        </span>
        <span class="icon-text">
          <span class="icon"><i class="fas fa-paper-plane"></i></span>
          <span>{post.shares ?? 0}</span>
        </span>
      </div>

      <!-- recent comment ยังไม่ได้แก้ให้เลือกได้-->
      <div style="border-top: 1px solid #eaeaea; border-bottom: 1px solid #eaeaea; padding: 8px 0; display:flex; gap:16px;">
        <p class="mt-2 mb-2">Recent</p>
      </div>

      <!-- คอมเมนต์ static ของแต่ละโพส -->
      {#each post.staticComments as c}
        <article class="media">
          <figure class="media-left">
            <p class="image is-48x48">
              <img class="is-rounded" src={c.avatar}
                style="object-fit: cover; width:100%; height:100%;" />
            </p>
          </figure>
          <div class="media-content">
            <div class="content">
              <p><strong>{c.name}</strong><br>{c.text}<br>
                <small><a>Like</a> · <a>Reply</a> · {c.time}</small></p>
            </div>
          </div>
        </article>
      {/each}

    
      <!-- คอมเมนต์ dynamic จาก user -->
      {#each comments as comment}
        <article class="media">
          
          <figure class="media-left">
            <p class="image is-48x48">
              {#if $currentUser?.avatar}
                <img class="is-rounded" src={$currentUser.avatar}
                  style="object-fit: cover; width:100%; height:100%;" />
              {:else}
                <span style="width:48px; height:48px; background:#e0e0e0; border-radius:50%; display:flex; align-items:center; justify-content:center;">
                  <i class="fas fa-user"></i>
                </span>
              {/if}
            </p>
          </figure>
          <div class="media-content">
            <div class="content">
              <p><strong>{$currentUser?.name ?? 'You'}</strong><br>{comment}</p>
            </div>
          </div>
        </article>
      {/each}

      <!-- กล่องพิมพ์คอมเมนต์ใหม่ -->
      <article class="media">
        <figure class="media-left">
          <p class="image is-48x48">
            {#if $currentUser?.avatar}
              <img class="is-rounded" src={$currentUser.avatar}
                style="object-fit: cover; width:100%; height:100%;" />
            {:else}
              <span style="width:48px; height:48px; background:#e0e0e0; border-radius:50%; display:flex; align-items:center; justify-content:center;">
                <i class="fas fa-user"></i>
              </span>
            {/if}
          </p>
        </figure>

        <div class="media-content">
          <div class="field">
            <p class="control">
              <textarea class="textarea" bind:value={commentText} placeholder="Add a comment..."></textarea>
            </p>
          </div>
          <div class="field">
            <p class="control">
              <button class="button is-primary is-rounded" on:click={postComment}>
                Post comment
              </button>
            </p>
          </div>
        </div>
      </article>

    </div>
  </div>
</section>

{/if}

<style>
  .tag-filter-box{
    background: white;
    border-top: 1px solid #eaeaea;
    border-bottom: 1px solid #eaeaea;
    padding: 16px 0;
    position: sticky;
    top: 0;
    z-index: 30;
  }
  .tag { cursor: pointer; }
  .tag:hover { opacity: 0.85; }
</style>