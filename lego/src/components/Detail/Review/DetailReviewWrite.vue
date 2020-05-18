<template>
  <div id="detail-review-write">
    <input
      type="Number"
      step="1"
      min="0"
      max="5"
      v-model="params.score"
      id="detail-review-score"
    />
    <textarea
      cols="100"
      rows="2"
      id="detail-review-textarea"
      @keydown="textareaResize()"
      @keyup="textareaResize()"
      v-model="params.content"
      placeholder=" 리뷰리뷰리뷰"
    ></textarea>
    <input type="submit" @click="onSubmit()" id="detail-review-submit" />
  </div>
</template>

<script>
export default {
  data() {
    return {
      params: {
        score: 0,
        content: ""
      }
    };
  },
  methods: {
    textareaResize() {
      const target = document.getElementById("detail-review-textarea");
      target.style.height = "20px";
      target.style.height = 12 + target.scrollHeight + "px";
    },
    onSubmit() {
      console.log(this.params);
    }
  }
};
</script>

<style scoped>
#detail-review-write {
  border: 1px solid gold;
  padding: 10px;
  display: flex;
  margin-bottom: 20px;
}
#detail-review-score {
  font-size: 40px;
  text-align: center;
  width: 70px;
  height: 70px;
  border: 1px solid black;
  margin-right: 10px;
  cursor: pointer;
}
#detail-review-textarea {
  resize: vertical;
  overflow: visible;
  border: 1px solid black;
  margin-right: 10px;
}
#detail-review-submit {
  font-size: 24px;
  text-align: center;
  width: 70px;
  height: 70px;
  border: 1px solid black;
}
</style>
