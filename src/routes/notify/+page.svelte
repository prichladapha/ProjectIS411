<script>
  let notifications = [
    {
      title: "Order 43827 : Uncle's Sneaker",
      subtitle: "your order status has been updated",
      detail: "check your order here!",
      count: 1,
      time: "1 hr ago",
    },
    {
      title: "Order 43827 : เสื้อ polo สีกรม ปักม้าแดง",
      subtitle: "your order status has been updated",
      detail: "check your order here!",
      count: 1,
      time: "2 hrs ago",
    },
    {
      title: "พั้นคุง commented on your post",
      subtitle: "ช่วย match หน่อยค่ะ อยากได้กระโปรงสวยๆ",
      detail: "ลองใส่กับสูทสีน้ำรักๆใหมคะ",
      count: 3,
      time: "3 hrs ago",
    },
    {
      title: "น้องผัก commented on your post",
      subtitle: "ช่วย match หน่อยค่ะ อยากได้กระโปรงสวยๆ",
      detail: "แนะนำให้ใส่กับสีอ่อนนุ่มนวลคนสวย",
      count: null,
      time: "2 hrs ago",
      link: "/postdetail?id=1"
    }
  ];
</script>

<div class="container pt-5">
      <div class="level-left">
        <div class="level-item">
          <h1 class="title is-4">Notification</h1>
        </div>
        </div>
</div>

{#each notifications as noti}
<div class="container mt-3">
  <a href={noti.link} style="text-decoration: none; color: inherit;">
    <div class="box mb-3 px-4 py-4 has-background-light">
      <div class="is-flex is-justify-content-space-between is-align-items-center">
        <div class="is-flex-grow-1 mr-4">
          <p class="mb-1"><strong>{noti.title}</strong></p>
          <p class="is-size-6 has-text-grey mb-1">{noti.subtitle}</p>
          <p class="is-size-7 has-text-grey">{noti.time}</p>
        </div>

        <!-- Badge -->
        {#if noti.count}
    <span class="tag is-rounded has-background-primary has-text-white has-text-weight-bold">
    {noti.count}
    </span>
        {/if}

      </div>
    </div>
</div>
{/each}