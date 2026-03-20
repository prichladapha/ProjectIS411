<script>
  import { goto } from '$app/navigation';

  let posts = [
    {
      name: "ลีน่าจัง",
      username: "@kikidoyouloveme",
      avatar: "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQOxqzW9JSe7pOmbjCUXdlPxBzEvkhKBUrI5g&s",
      content: "เสื้อแบบนี้ใส่กับกระโปรงแบบไหนดีคะ ของแบรนด์ @littlemonday #matching #whitetop",
      image: "https://i.pinimg.com/1200x/6a/ae/d0/6aaed02da72d5373c07eaf7b69116a8b.jpg",
      likes: 24, reposts: 5, shares: 2,
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
      likes: 10, reposts: 2, shares: 1,
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
      likes: 55, reposts: 12, shares: 4,
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
      likes: 30, reposts: 3, shares: 2,
      staticComments: [
        { name: "เย้ๆๆๆ", avatar: "https://i.pinimg.com/1200x/bb/10/5a/bb105a7c0fa94cfce7a2ec8fc4dc5d55.jpg", text: "ได้มาจากที่ไหนคะ", time: "2 hrs" }
      ]
    }

  // รัน id อัตโนมัติ และนับ comments จาก staticComments
  ].map((post, index) => ({ ...post, id: index + 1, comments: post.staticComments.length }))
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
  {#each posts as post}
  <!-- กดการ์ดแล้วไปหน้า postdetail พร้อมส่ง id -->
  <div class="card mb-4" style="max-width:1400px; margin:auto; cursor:pointer;"
    on:click={() => goto(`/postdetail?id=${post.id}`)}>
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