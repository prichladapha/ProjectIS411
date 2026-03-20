

<!-- หน้า Post Detail — แสดงโพสที่กดมาจากฟีด พร้อมคอมเมนต์ -->
<script>
  import { page } from '$app/stores';
  import { currentUser } from '$lib/shared';

  // ข้อมูลโพสทั้งหมด ตามหน้าฟีด
  const posts = [
    {
      name: "ลีน่าจัง",
      username: "@kikidoyouloveme",
      avatar: "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQOxqzW9JSe7pOmbjCUXdlPxBzEvkhKBUrI5g&s",
      content: "เสื้อแบบนี้ใส่กับกระโปรงแบบไหนดีคะ ของแบรนด์ @littlemonday #matching #whitetop",
      image: "https://i.pinimg.com/1200x/6a/ae/d0/6aaed02da72d5373c07eaf7b69116a8b.jpg",
      staticComments: [
        { name: "พั้นคุง", avatar: "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRZi_CHzIU68gmOMxUUtfMQUtDKnC9B_s4mHA&s", text: "ใส่กะกระโปรงสีอ่อนๆมั้ยค้าฟคนสวย", time: "3 hrs" },
        { name: "น้องผัก", avatar: "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTyszNIwM59Yja6anjgdZoSeP6XACdto22acQ&s", text: "กระโปรงสั้นๆก็สวยน้าอ้วน", time: "2 hrs" },
        { name: "มาดามจือ", avatar: "https://hauterrfly.com/wp-content/uploads/2025/10/aespa-giselle-tattoo-backlash-misogynistic-backlash.jpg", text: "ขอพิกัดได้มั้ยคะ", time: "2 hrs" }
      ]
    },
    {
      name: "น้องผัก",
      username: "@veggie_girl",
      avatar: "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTyszNIwM59Yja6anjgdZoSeP6XACdto22acQ&s",
      content: "เอ้าฟิตวันนี้ค่ะ เสื้อ40 ส่วนกระโปรงยืมแม่ #ootd #vintage",
      image: "https://i.pinimg.com/736x/33/de/7e/33de7e83f418c4ff2f3f50591748f702.jpg",
      staticComments: [
        { name: "ลีน่าจัง", avatar: "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQOxqzW9JSe7pOmbjCUXdlPxBzEvkhKBUrI5g&s", text: "น่ารักมากเลยค่า", time: "1 hr" }
      ]
    },
    {
    name: "เย้ๆๆๆ",
    username: "@yippeee",
    avatar: "https://i.pinimg.com/1200x/bb/10/5a/bb105a7c0fa94cfce7a2ec8fc4dc5d55.jpg",
    content: "Y2K fit of the day 🤍 #y2k #fashion",
    image: "https://i.pinimg.com/1200x/4c/d9/79/4cd97954db08a8dc48a9bd6e59e1c378.jpg",
    staticComments: [
      { name: "rosie", avatar: "https://i.pinimg.com/736x/08/01/e2/0801e233c0533e1fbfbab744b9155d57.jpg", text: "cute มากเลยค่า", time: "1 hr" }
    ]
  },
  {
    name: "rosie",
    username: "@imnaim_",
    avatar: "https://i.pinimg.com/736x/08/01/e2/0801e233c0533e1fbfbab744b9155d57.jpg",
    content: "vintage haul มาค่ะ ได้มาจากตลาดนัด #vintage #thrift",
    image: "https://i.pinimg.com/1200x/a3/14/b3/a314b3f341ba3d4e8bfee915ad6a9c0f.jpg",
    staticComments: [
      { name: "เย้ๆๆๆ", avatar: "https://i.pinimg.com/1200x/bb/10/5a/bb105a7c0fa94cfce7a2ec8fc4dc5d55.jpg", text: "ได้มาจากที่ไหนคะ", time: "2 hrs" },
      { name: "มาดามจือ", avatar: "https://hauterrfly.com/wp-content/uploads/2025/10/aespa-giselle-tattoo-backlash-misogynistic-backlash.jpg", text: "เมนท์บนได้อ่านแคปชันมั้ยคะ", time: "2 hrs" }
    ]
  }
  // รัน id อัตโนมัติ
  ].map((post, index) => ({ ...post, id: index + 1 }))

  // ดึง id จาก URL แล้วหาโพสที่ตรงกัน
 $: id = Number($page.url.searchParams.get('id'));
  $: post = posts.find(p => p.id === id);

  // กดpost commentเม้นแล้วขึ้นเม้นใหม่
  let commentText = "";
  let comments = [];

  function postComment() {
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

      <!-- จำนวนคอมเมนต์ -->
      <p class="has-text-weight-bold mt-3">
        <span class="icon"><i class="fas fa-comment"></i></span>
        {post.staticComments.length + comments.length} comments
      </p>
      <p class="mt-2 mb-2">Recent</p>

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
              <img class="is-rounded" 
                src={$currentUser?.avatar || 'default'}
                style="object-fit: cover; width:100%; height:100%;" />
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
            <img class="is-rounded" src={$currentUser?.avatar}
              style="object-fit: cover; width:100%; height:100%;" />
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