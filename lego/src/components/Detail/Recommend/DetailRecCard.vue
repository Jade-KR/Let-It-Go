<template>
  <div class="rec_card_main">
    <div>
      <img src="../../../assets/login_bg.jpg" alt="image" class="rec_img" />
    </div>
    <div class="rec_card_info">
      <div class="rec_card_box">
        <!-- <div class="rec_card_name">NAME NAME NAMENAME NAME NAME</div> -->
        <div class="rec_card_name">NAME NAME</div>
        <div class="rec_card_bricks">By. 이상해씨꼬부기파이리삐까</div>
        <div class="rec_card_icon">
          <i
            class="fas fa-heart"
            :style="isLike === 1 ? likeStyle[0] : likeStyle[1]"
          ></i>
          <!-- <span>{{ likeCount }}</span> -->
          <span style="margin-right: 15px;">12</span>
          <i
            class="fas fa-comment"
            :style="isReview === 1 ? reviewStyle[0] : reviewStyle[1]"
          ></i>
          <!-- <span>{{ reviewCount }}</span> -->
          <span>142</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      isLike: 1,
      isReview: 1,
      likeStyle: [
        {
          color: "red"
        },
        {
          color: "white"
        }
      ],
      reviewStyle: [
        {
          color: "gold"
        },
        {
          color: "white"
        }
      ]
    };
  }
};
</script>

<style scoped>
.rec_card_main {
  text-align: center;
  height: 200px;
}
.rec_img {
  width: 200px;
  height: 200px;
}
.rec_card_info {
  width: 200px;
  height: 200px;
  color: white;
  background-color: rgba(0, 0, 0, 0.5);
  position: absolute;
  transform: translate(18px, -207px);
  transition: 0.3s ease;
  opacity: 0;
  cursor: pointer;
  display: table;
}
.rec_card_info:hover {
  opacity: 1;
}
.rec_card_box {
  display: table-cell;
  vertical-align: middle;
}
.rec_card_name {
  font-size: 20px;
}
.rec_card_bricks {
  font-size: 14px;
}
.rec_card_icon {
  font-size: 25px;
}
</style>
