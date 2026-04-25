<script>
  import { goto } from '$app/navigation';
  import { posts } from '../postdetail/data.js';
</script>


<section class="section pt-3">

  <!-- loop วนแสดงโพสทุกอัน -->
<div class="mt-4">
  {#each posts as post (post.id)}
  <!-- กดการ์ดแล้วไปหน้า postdetail พร้อมส่ง id -->
  <div class="card mb-3 post-card" style="cursor:pointer;"
    on:click={() => goto(`/postdetail/${post.id}`)}>
    <div class="card-content">

      <!-- ข้อมูลคนโพส -->
      <div class="is-flex is-align-items-center mb-2">
        <figure class="image is-32x32 mr-2">
          <img class="is-rounded" src={post.avatar}
            style="object-fit:cover; width:100%; height:100%;">
        </figure>
        <div>
          <p style="font-size:0.85rem; font-weight:600; margin:0;">{post.name}</p>
          <p style="font-size:0.75rem; color:#888; margin:0;">{post.username}</p>
        </div>
      </div>

      <!-- เนื้อหาโพส -->
      <p style="font-size:0.85rem; margin-bottom:10px;">{post.content}</p>

      <!-- Horizontal Carousel รูปภาพ -->
      <!-- Horizontal Carousel รูปภาพ -->
      <div style="display:flex; justify-content:center; overflow-x:auto; gap:8px; scroll-snap-type:x mandatory; -webkit-overflow-scrolling:touch;">
        <img src={post.image} alt="post"
          style="aspect-ratio:4/5; width:260px; border-radius:8px; flex-shrink:0; scroll-snap-align:start; object-fit:cover;" />
      </div>

      <!-- ไอคอน reaction -->
      <div class="is-flex mt-2" style="justify-content:space-between;">
        <span class="icon-text" style="font-size:0.8rem;">
          <span class="icon is-small"><i class="fas fa-heart"></i></span>
          <span>{post.likes}</span>
        </span>
        <span class="icon-text" style="font-size:0.8rem;">
          <span class="icon is-small"><i class="fas fa-comment"></i></span>
          <span>{post.comments}</span>
        </span>
        <span class="icon-text" style="font-size:0.8rem;">
          <span class="icon is-small"><i class="fas fa-retweet"></i></span>
          <span>{post.reposts}</span>
        </span>
        <span class="icon-text" style="font-size:0.8rem;">
          <span class="icon is-small"><i class="fas fa-paper-plane"></i></span>
          <span>{post.shares}</span>
        </span>
      </div>
     </div>
    </div>
  {/each}
</div>

<!-- ปุ่มโพสมุมขวาล่าง ยังไม่มีหน้า/createpost-->
<button class="button is-primary is-rounded"
  style="position:fixed; bottom:32px; right:32px; width:56px; height:56px; border-radius:50%; font-size:24px; box-shadow: 0 4px 12px rgba(0,0,0,0.2);"
  on:click={() => goto('/createpost')}>
  <span class="icon">
    <i class="fas fa-plus"></i>
  </span>

</section>

<style>
 .post-card {
    max-width: 520px;
    width: 100%;
    margin: 0 auto 12px auto;
    cursor: pointer;
    border-radius: 12px;
    border: 1px solid #efefef;
    transition: background-color 0.2s ease;
  }

  .post-card:hover {
    background-color: #f9f9f9;
  }

  .tag-filter-box {
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
