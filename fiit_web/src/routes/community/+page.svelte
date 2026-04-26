<script>
  import { goto } from '$app/navigation';
  let { data } = $props(); 
  // ใช้ $derived เพื่อให้ตัวแปร posts อัปเดตตาม data เสมอ
  let posts = $derived(data.posts || []);
</script>

<section class="section pt-3">
  <div class="mt-4">
    {#each posts as post (post.id)}
      <div class="card mb-3 post-card" style="cursor:pointer;"
        on:click={() => goto(`/postdetail/${post.id}`)}>
        <div class="card-content">

          <div class="is-flex is-align-items-center mb-2">
            <figure class="image is-32x32 mr-2">
              <img class="is-rounded" src={post.avatar} alt="avatar" style="object-fit:cover; width:32px; height:32px;">
            </figure>
            <div>
              <p style="font-size:0.85rem; font-weight:600; margin:0;">{post.name}</p>
              <p style="font-size:0.75rem; color:#888; margin:0;">{post.username}</p>
            </div>
          </div>

          <p style="font-size:0.85rem; margin-bottom:10px;">{post.content}</p>

          <div style="display:flex; justify-content:center;">
            <img src={post.image} alt="post"
              style="aspect-ratio:4/5; width:260px; border-radius:8px; object-fit:cover;" />
          </div>

          <div class="is-flex mt-3" style="justify-content:space-between;">
            <span class="icon-text" style="font-size:0.8rem;">
              <span class="icon is-small has-text-danger"><i class="fas fa-heart"></i></span>
              <span>{post.likes}</span>
            </span>
            
            <span class="icon-text" style="font-size:0.8rem;">
              <span class="icon is-small has-text-info"><i class="fas fa-comment"></i></span>
              <span>{post.comments_count}</span>
            </span>

            <span class="icon-text" style="font-size:0.8rem;">
              <span class="icon is-small has-text-success"><i class="fas fa-retweet"></i></span>
              <span>{post.reposts}</span>
            </span>

            <span class="icon-text" style="font-size:0.8rem;">
              <span class="icon is-small has-text-grey"><i class="fas fa-paper-plane"></i></span>
              <span>{post.shares}</span>
            </span>
          </div>
          
        </div>
      </div>
    {/each}
  </div>

  <button class="button is-primary is-rounded floating-btn" on:click={() => goto('/createpost')}>
    <span class="icon"><i class="fas fa-plus"></i></span>
  </button>
</section>

<style>
  .post-card { 
    max-width: 520px; 
    margin: 0 auto 12px auto; 
    border-radius: 12px; 
    border: 1px solid #efefef; 
    transition: background-color 0.2s;
  }
  .post-card:hover {
    background-color: #fafafa;
  }
  .floating-btn { 
    position:fixed; 
    bottom:32px; 
    right:32px; 
    width:56px; 
    height:56px; 
    border-radius:50%; 
    box-shadow: 0 4px 10px rgba(0,0,0,0.1);
    z-index: 99;
  }
</style>
