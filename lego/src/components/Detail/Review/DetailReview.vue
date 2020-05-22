<template>
  <div class="detail-review-card">
    <div class="detail-review-show">
      <img
        src="../../../../public/images/user.png"
        alt="img"
        class="detail-review-img"
      />
      <div class="rating">
        <div @click="rating()">
          asdf
        </div>
        <div @click="input()">
          zxcv
        </div>
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
    <div class="detail-review-desc">
      <div class="detail-review-info">
        <div class="detail-review-id">
          빨갛게빛나는나까무라상
        </div>
        <div class="detail-review-date">
          2020-05-13
        </div>
      </div>
      <div class="detail-review-content">
        Lorem Ipsum is simply dummy text of the printing and typesetting
        industry. Lorem Ipsum has been the industry's standard dummy text ever
        since the 1500s, when an unknown printer took a galley of type and
        scrambled it to make a type specimen book. It has survived not only five
        centuries, but also the leap into electronic typesetting, remaining
        essentially unchanged. It was popularised in the 1960s with the release
        of Letraset sheets containing Lorem Ipsum passages, and more recently
        with desktop publishing software like Aldus PageMaker including versions
        of Lorem Ipsum
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      ratingTest: 0
    };
  },
  methods: {
    rating() {
      console.log(this.ratingTest);
    },
    input() {
      this.ratingTest = 3;
      console.log(this.ratingTest);
    }
  }
};
</script>

<style scoped>
.detail-review-card {
  display: flex;
  padding: 10px;
  border: 1px solid gold;
}
.detail-review-show {
  flex: 1;
}
.detail-review-img {
  width: 100px;
  height: 100px;
  margin-right: 10px;
  border-radius: 50%;
}
.detail-review-desc {
  flex: 9;
}
.detail-review-info {
  display: block;
  margin-bottom: 5px;
}
.detail-review-id {
  display: inline-block;
  font-size: 20px;
  margin-right: 10px;
}
.detail-review-date {
  display: inline-block;
  color: rgba(128, 128, 128, 0.7);
}
.detail-review-content {
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
