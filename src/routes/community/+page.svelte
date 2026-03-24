<script>
  import { goto } from '$app/navigation';
  import { posts } from '../postdetail/data.js';
</script>


<section class="section pt-3">

  <!-- แถบ TAGS ติดด้านบน -->
  <div class="container">
    <div class="tag-filter-box">
      <div class="container" style="max-width:1400px;">
        <div class="is-flex is-align-items-center is-flex-wrap-wrap">
          <p class="title is-5 mr-4 mb-2">TAGS</p>
          <div class="field is-grouped is-grouped-multiline">
            <div class="control"><span class="tag is-success is-medium">Woman</span></div>
            <div class="control"><span class="tag is-success is-medium">Men</span></div>
            <div class="control"><span class="tag is-success is-medium">Vintage</span></div>
            <div class="control"><span class="tag is-success is-medium">Y2K</span></div>
            <div class="control"><span class="tag is-success is-medium">Others</span></div>
          </div>
        </div>
      </div>
    </div>
  </div>

  <!-- loop วนแสดงโพสทุกอัน -->
  {#each posts as post (post.id)}
  <!-- กดการ์ดแล้วไปหน้า postdetail พร้อมส่ง id -->
  <div class="card mb-4" style="max-width:1400px; margin:auto; cursor:pointer;"
    on:click={() => goto(`/postdetail/${post.id}`)}>
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
            style="width:100%; height:auto; max-height:500px; object-fit:cover; border-radius:8px;" />
        </figure>
      </div>

      <!-- ไอคอน reaction -->
      <div class="is-flex is-align-items-center mt-3" style="gap: 24px;">
        <span class="icon-text">
          <span class="icon"><i class="fas fa-heart"></i></span>
          <span>{post.likes}</span>
        </span>
        <span class="icon-text">
          <span class="icon"><i class="fas fa-comment"></i></span>
          <span>{post.comments}</span>
        </span>
        <span class="icon-text">
          <span class="icon"><i class="fas fa-retweet"></i></span>
          <span>{post.reposts}</span>
        </span>
        <span class="icon-text">
          <span class="icon"><i class="fas fa-paper-plane"></i></span>
          <span>{post.shares}</span>
        </span>
      </div>

    </div>
  </div>
  {/each}

</section>

<style>
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