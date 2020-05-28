<template>
  <div class="detail_review_card">
    <div class="detail_review_show">
      <img
        :src="userImage"
        alt="user_image"
        class="detail_review_img"
        v-if="userImage !== 'null'"
      />
      <img
        src="../../../../public/images/user.png"
        alt="img"
        class="detail_review_img"
        v-else
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
          {{ time }}
        </div>
        <div class="review_update" v-if="isMe === true">
          <i class="fas fa-pen" @click="isUpdate()"></i>
        </div>
        <div class="review_delete" v-if="isMe === true">
          <i class="fas fa-trash-alt" @click="onDelete()"></i>
        </div>
      </div>
      <div class="detail_review_content" v-if="updateFlag === false">
        <div v-for="(sentence, i) in sentences" :key="i">
          {{ sentence }}
        </div>
      </div>
      <div class="detail_review_content" v-else>
        <textarea
          cols="100"
          rows="2"
          id="detail-review-textarea"
          v-model="sentences"
        >
        </textarea>
      </div>
    </div>
  </div>
</template>

<script>
import router from "../../../router";
import { mapActions } from "vuex";

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
    userId: {
      type: Number,
      default: 0
    },
    reviewId: {
      type: Number,
      default: 0
    },
    updatedAt: {
      type: String,
      default: ""
    },
    userImage: {
      type: String,
      default: ""
    },
    setId: {
      type: Number,
      default: 0
    }
  },
  data() {
    return {
      ratingTest: 0,
      time: "",
      sentences: "",
      isMe: false,
      updateFlag: false
    };
  },
  mounted() {
    this.ratingTest = this.score;
    this.time =
      this.updatedAt.slice(0, 10) + " " + this.updatedAt.slice(11, 19);
    if (this.content !== null) {
      this.sentences = this.content.split("\n");
    }
    if (this.userId === Number(localStorage.getItem("pk"))) {
      this.isMe = true;
    }
  },
  methods: {
    ...mapActions("detail", ["reviewUpdate", "reviewDelete"]),
    goYourPage() {
      router.push("/mypage/" + this.userId);
    },
    isUpdate() {
      this.updateFlag = true;
    },
    async onUpdate() {
      const params = {
        id: this.reviewId
      };
      await this.reviewUpdate(params);
    },
    async onDelete() {
      const params = {
        id: this.reviewId,
        lego_set_id: this.setId
      };
      await this.reviewDelete(params);
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
  margin-right: 10px;
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
.review_update,
.review_delete {
  cursor: pointer;
  display: inline-block;
  margin-right: 10px;
}
</style>
