<template>
  <div class="detail_review_card">
    <div class="detail_review_show">
      <img
        src="../../../../public/images/user.png"
        alt="img"
        class="detail_review_img"
      />
      <div class="rating">
        <fieldset class="rating">
          <input
            type="radio"
            id="star5"
            name="rating"
            value="5"
            v-model="ratingTest"
            disabled
          /><label class="full" for="star5" title="5 stars"></label>
          <input
            type="radio"
            id="star4"
            name="rating"
            value="4"
            v-model="ratingTest"
            disabled
          /><label class="full" for="star4" title="4 stars"></label>
          <input
            type="radio"
            id="star3"
            name="rating"
            value="3"
            v-model="ratingTest"
            disabled
          /><label class="full" for="star3" title="3 stars"></label>
          <input
            type="radio"
            id="star2"
            name="rating"
            value="2"
            v-model="ratingTest"
            disabled
          /><label class="full" for="star2" title="2 stars"></label>
          <input
            type="radio"
            id="star1"
            name="rating"
            value="1"
            v-model="ratingTest"
            disabled
          /><label class="full" for="star1" title="1 star"></label>
        </fieldset>
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
    console.log("score", this.score);
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

@import url(//netdna.bootstrapcdn.com/font-awesome/3.2.1/css/font-awesome.css);
.rating {
  border: none;
  float: left;
}
.rating > input {
  display: none;
}
.rating > label:before {
  font-size: 1.25em;
  font-family: FontAwesome;
  display: inline-block;
  content: "\f005";
}
.rating > label {
  color: #ddd;
  float: right;
}
.rating > input:checked ~ label,
.rating:not(:checked) > label,
.rating:not(:checked) > label ~ label {
  color: #ddd;
}
.rating > input:checked + label,
.rating > input:checked ~ label,
.rating > label ~ input:checked ~ label,
.rating > input:checked ~ label ~ label {
  color: gold;
}
</style>
