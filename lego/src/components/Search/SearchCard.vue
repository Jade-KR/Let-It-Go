<template>
  <div class="item" @click="goDetail()">
    <div class="body_img_box">
      <img
        class="body_img"
        src="../../assets/icons/no_img.jpg"
        alt="no_image"
        v-if="image === null || image === '' || errorFlag === true"
      />
      <img
        class="body_img"
        :src="image"
        alt="image"
        v-else
        @error="imgError()"
      />

      <div class="body_img_hover">
        <div class="body_img_desc">
          <div class="body_img_name">
            <b>{{ name }}</b>
          </div>
          <div class="body_img_nick">By. {{ nickname }}</div>
          <div class="body_img_info">
            <i
              class="fas fa-heart"
              :style="isLike === 1 ? likeStyle[0] : likeStyle[1]"
            ></i>
            <span>{{ likeCount }}</span>
            <i
              class="fas fa-comment"
              :style="isReview === 1 ? reviewStyle[0] : reviewStyle[1]"
            ></i>
            <span>{{ reviewCount }}</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import router from "../../router";

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
    },
    isLike: {
      type: Number,
      default: 0
    },
    likeCount: {
      type: Number,
      default: 0
    },
    reviewCount: {
      type: Number,
      default: 0
    },
    isReview: {
      type: Number,
      default: 0
    }
  },
  data() {
    return {
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
      ],
      errorFlag: false
    };
  },
  methods: {
    goDetail() {
      router.push("/detail/" + this.id);
      window.scrollTo(0, 0);
    },
    imgError() {
      this.errorFlag = true;
    }
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
  /* display: flex; */
  display: table;
  align-items: center;
}
.body_img_desc {
  display: table-cell;
  vertical-align: middle;
  color: white;
  text-align: center;
}
.body_img_name {
  font-size: 24px;
}
.body_img_nick {
  font-size: 16px;
  margin-bottom: 15px;
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
  display: flex;
  justify-content: center;
  align-items: baseline;
  transform: translate(10px, -10px);
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

@media screen and (max-width: 600px) {
  .item {
    width: 33.3vw;
    height: 33.3vw;
    margin: 0;
  }
  .body_img_hover {
    display: none;
  }
}
</style>
