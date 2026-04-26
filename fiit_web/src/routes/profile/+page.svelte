<script>
  import { enhance } from '$app/forms';

  let { data } = $props();
  let user = data.user;
  let extraInfo = {
    bio: 'ชอบแต่งตัวแนววินเทจ มือสองน่ารัก ๆ 🌷',
    location: 'Bangkok, Thailand'
  };

  let stats = {
    posts: 1,
    followers: 127,
    following: 87
  };

  let posts = [
    {
      content: 'เอ้าฟิตวันนี้ค่ะ เสื้อ40 ส่วนกระโปรงยืมแม่ #ootd #vintage',
      image: 'https://i.pinimg.com/736x/33/de/7e/33de7e83f418c4ff2f3f50591748f702.jpg'
    }
  ];
</script>

<section class="section">
  <div class="container">
    <div class="columns is-vcentered">
      <div class="column is-4 has-text-centered">
        <figure
          class="image is-128x128 is-inline-block"
          style="overflow: hidden; border-radius: 50%;"
        >
          <img
            src={user.avatar || 'https://www.gravatar.com/avatar/00000000000000000000000000000000?d=mp&f=y'}
            alt={user.display_name || user.username}
            style="width: 100%; height: 100%; object-fit: cover;"
          />
        </figure>
      </div>

      <div class="column is-8">
        <div class="is-flex is-align-items-center is-flex-wrap-wrap mb-4">
          <p class="title is-4 mr-4 mb-2">@{user.display_name || user.username}</p>

          <div class="buttons mb-2">
            <button class="button is-primary is-light">Edit profile</button>
            <button class="button is-light">Share profile</button>
            <a class="button is-light" href="/myshop">My Shop</a>
            <a class="button is-light" href="/myorder">My Order</a>
            
            <form action="?/logout" method="POST" use:enhance class="ml-2">
              <button class="button is-danger is-outlined" type="submit">
                Log out
              </button>
            </form>
          </div>
        </div>

        <div class="columns is-mobile mb-4">
          <div class="column">
            <p><strong>{stats.posts}</strong> posts</p>
          </div>
          <div class="column">
            <p><strong>{stats.followers}</strong> followers</p>
          </div>
          <div class="column">
            <p><strong>{stats.following}</strong> following</p>
          </div>
        </div>

        <div class="content">
          <p class="has-text-weight-semibold mb-1">
            {user.display_name || user.username} 
            <span class="has-text-grey is-size-7">({user.email})</span>
          </p>
          <p class="is-size-7 has-text-grey mb-2">📞 {user.customer_phone}</p>
          <p class="mb-1">{extraInfo.bio}</p>
          <p class="has-text-grey">{extraInfo.location}</p>
        </div>
      </div>
    </div>

    <hr />

    <div class="tabs is-centered is-boxed">
      <ul>
        <li class="is-active"><a>POSTS</a></li>
        <li><a>TAGGED</a></li>
      </ul>
    </div>

    <div class="columns is-multiline is-mobile">
      {#each posts as post}
        <div class="column is-12-mobile is-6-tablet is-4-desktop">
          <div class="card">
            <div class="card-image">
              <figure class="image is-square" style="overflow: hidden;">
                <img
                  src={post.image}
                  alt="post"
                  style="width: 100%; height: 100%; object-fit: cover;"
                />
              </figure>
            </div>

            <div class="card-content">
              <p class="has-text-weight-semibold">@{user.display_name || user.username}</p>
              <p class="mt-2">{post.content}</p>
            </div>
          </div>
        </div>
      {/each}
    </div>
  </div>
</section>