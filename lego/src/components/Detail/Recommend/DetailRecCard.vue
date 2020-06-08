<template>
  <div class="rec_card_main" @click="goDetail(id)">
    <div>
      <img
        :src="`${images}`"
        alt="image"
        class="rec_img"
        @error="imgError()"
        v-if="imgFlag === true"
      />
      <img
        src="../../../assets/icons/no_img.jpg"
        alt="no_image"
        class="rec_img"
        v-else
      />
    </div>
    <div class="rec_card_info">
      <div class="rec_card_box">
        <div class="rec_card_name">{{ name }}</div>
        <div class="rec_card_bricks">By. {{ nickname }}</div>
        <div class="rec_card_icon">
          <i
            class="fas fa-heart"
            :style="isLike === 1 ? likeStyle[0] : likeStyle[1]"
          ></i>
          <span style="margin-right: 15px;">{{ likeCount }}</span>
          <i
            class="fas fa-comment"
            :style="isReview === 1 ? reviewStyle[0] : reviewStyle[1]"
          ></i>
          <span>{{ reviewCount }}</span>
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
    name: {
      type: String,
      default: ""
    },
    images: {
      type: String,
      default: ""
    },
    nickname: {
      type: String,
      default: ""
    },
    isLike: {
      type: Number,
      default: -1
    },
    isReview: {
      type: Number,
      default: -1
    },
    likeCount: {
      type: Number,
      default: 0
    },
    reviewCount: {
      type: Number,
      default: 0
    }
  },
  data() {
    return {
      imgFlag: true,
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
  },
  methods: {
    goDetail(value) {
      const toPath = Number(value);
      const now = Number(this.$route.params.modelId);
      if (toPath === now) {
        return;
      }
      this.$router.push("/detail/" + value);
      window.scrollTo(0, 0);
    },
    imgError() {
      this.imgFlag = false;
    }
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
  border: 0.5px solid gold;
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

@media screen and (max-width: 600px) {
  .rec_card_main {
    height: 100%;
  }
  .rec_img {
    width: 47vw;
    height: 47vw;
  }
  .rec_card_info {
    display: none;
  }
}
</style>
