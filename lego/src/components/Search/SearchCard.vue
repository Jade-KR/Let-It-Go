<template>
  <div class="item">
    <div class="body_img_box">
      <img class="body_img" :src="image" alt />
      <div class="body_img_hover">
        <div class="body_img_info">
          <i class="fas fa-heart"></i>
          <span>0</span>
          <i class="fas fa-comment"></i>
          <span>0</span>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
export default {
  props: {
    id: {
      type: Number,
      default: 0
    },
    image: {
      type: String,
      default: ""
    },
    name: {
      type: String,
      default: ""
    },
    nickname: {
      type: String,
      default: ""
    }
  },
  data() {
    return {};
  }
};
</script>

<style scoped>
.item {
  width: 260px;
  height: 250px;
  margin-left: 10px;
  margin-right: 10px;
}
.body_img_box {
  width: 100%;
  height: 100%;
  background: black;
  position: relative;
}
.body_img_box > img {
  width: 100%;
  height: 100%;
  /* border-radius: 180%; */
}
.body_img_hover {
  transition: 0.5s ease;
  opacity: 0;
  position: absolute;
  left: 50%;
  transform: translate(-50%, -90%);
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
}
.body_img {
  opacity: 1;
  cursor: pointer;
  transition: 0.5s ease;
}
.body_img_box:hover .body_img {
  opacity: 0.5;
  cursor: pointer;
}
.body_img_box:hover .body_img_hover {
  opacity: 1;
  cursor: pointer;
  transform: translate(-50%, -100%);
}
.body_img_info {
  width: 100%;
  text-align: center;
  position: absolute;
  display: flex;
  justify-content: center;
  align-items: baseline;
}
.body_img_info > i {
  font-size: 25px;
  color: white;
}
.body_img_info > span {
  margin-left: 10px;
  font-size: 25px;
  color: white;
  margin-right: 20px;
}
</style>
