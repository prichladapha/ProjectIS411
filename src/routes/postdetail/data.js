export const posts = [
  {
    name: "ลีน่าจัง",
    username: "@kikidoyouloveme",
    avatar: "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQOxqzW9JSe7pOmbjCUXdlPxBzEvkhKBUrI5g&s",
    content: "เสื้อแบบนี้ใส่กับกระโปรงแบบไหนดีคะ ของแบรนด์ @littlemonday #matching #whitetop",
    image: "https://i.pinimg.com/1200x/6a/ae/d0/6aaed02da72d5373c07eaf7b69116a8b.jpg",
    likes: 24,
    reposts: 5,
    shares: 2,
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
    likes: 10,
    reposts: 2,
    shares: 1,
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
    likes: 55,
    reposts: 12,
    shares: 4,
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
    likes: 30,
    reposts: 3,
    shares: 2,
    staticComments: [
      { name: "เย้ๆๆๆ", avatar: "https://i.pinimg.com/1200x/bb/10/5a/bb105a7c0fa94cfce7a2ec8fc4dc5d55.jpg", text: "ได้มาจากที่ไหนคะ", time: "2 hrs" },
      { name: "มาดามจือ", avatar: "https://hauterrfly.com/wp-content/uploads/2025/10/aespa-giselle-tattoo-backlash-misogynistic-backlash.jpg", text: "เมนท์บนได้อ่านแคปชันมั้ยคะ", time: "2 hrs" }
    ]
  }
].map((post, index) => ({
  ...post,
  id: index + 1,
  comments: post.staticComments.length
}));