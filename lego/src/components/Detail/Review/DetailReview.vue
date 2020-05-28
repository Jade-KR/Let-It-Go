<template>
  <div class="detail_review_card">
    <div class="detail_review_show">
      <img
        src="../../../../public/images/user.png"
        alt="img"
        class="detail_review_img"
      />
      <div class="rating">
        <div v-if="ratingTest === 5">
          <i class="fas fa-star gold_star"></i>
          <i class="fas fa-star gold_star"></i>
          <i class="fas fa-star gold_star"></i>
          <i class="fas fa-star gold_star"></i>
          <i class="fas fa-star gold_star"></i>
        </div>
        <div v-if="ratingTest === 4">
          <i class="fas fa-star gold_star"></i>
          <i class="fas fa-star gold_star"></i>
          <i class="fas fa-star gold_star"></i>
          <i class="fas fa-star gold_star"></i>
          <i class="fas fa-star gray_star"></i>
        </div>
        <div v-if="ratingTest === 3">
          <i class="fas fa-star gold_star"></i>
          <i class="fas fa-star gold_star"></i>
          <i class="fas fa-star gold_star"></i>
          <i class="fas fa-star gray_star"></i>
          <i class="fas fa-star gray_star"></i>
        </div>
        <div v-if="ratingTest === 2">
          <i class="fas fa-star gold_star"></i>
          <i class="fas fa-star gold_star"></i>
          <i class="fas fa-star gray_star"></i>
          <i class="fas fa-star gray_star"></i>
          <i class="fas fa-star gray_star"></i>
        </div>
        <div v-if="ratingTest === 1">
          <i class="fas fa-star gold_star"></i>
          <i class="fas fa-star gray_star"></i>
          <i class="fas fa-star gray_star"></i>
          <i class="fas fa-star gray_star"></i>
          <i class="fas fa-star gray_star"></i>
        </div>
        <div v-if="ratingTest === 0">
          <i class="fas fa-star gray_star"></i>
          <i class="fas fa-star gray_star"></i>
          <i class="fas fa-star gray_star"></i>
          <i class="fas fa-star gray_star"></i>
          <i class="fas fa-star gray_star"></i>
        </div>
      </div>
    </div>
    <div class="detail_review_desc">
      <div class="detail_review_info">
        <div class="detail_review_id" @click="goYourPage()">
          {{ nickname }}
        </div>
        <div class="detail_review_date">
          2020-05-13
        </div>
      </div>
      <div class="detail_review_content">
        {{ content }}
      </div>
    </div>
    <div>
      <div>
        수정
      </div>
      <div>
        삭제
      </div>
    </div>
  </div>
</template>

<script>
import router from "../../../router";

export default {
  props: {
    content: {
      type: String,
      default: ""
    },
    nickname: {
      type: String,
      default: ""
    },
    score: {
      type: Number,
      default: 0
    },
    user_id: {
      type: Number,
      default: 0
    }
    // 시간, 이미지
  },
  data() {
    return {
      ratingTest: 0
    };
  },
  mounted() {
    this.ratingTest = this.score;
  },
  methods: {
    goYourPage() {
      router.push("/mypage/" + this.user_id);
    }
  }
};
</script>

<style scoped>
.detail_review_card {
  display: flex;
  padding: 10px;
  border: 1px solid gold;
}
.detail_review_show {
  flex: 1;
}
.detail_review_img {
  width: 100px;
  height: 100px;
  margin-right: 10px;
  border-radius: 50%;
}
.detail_review_desc {
  flex: 9;
}
.detail_review_info {
  display: block;
  margin-bottom: 5px;
}
.detail_review_id {
  display: inline-block;
  font-size: 20px;
  margin-right: 10px;
  cursor: pointer;
}
.detail_review_date {
  display: inline-block;
  color: rgba(128, 128, 128, 0.7);
}
.detail_review_content {
  display: inline-block;
}
.gold_star {
  color: gold;
}
.gray_star {
  color: gray;
}
</style>
