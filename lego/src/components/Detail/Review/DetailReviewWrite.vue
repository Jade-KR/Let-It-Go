<template>
  <div id="detail-review-write" v-if="isLogin">
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
      placeholder=" 리뷰를 작성해 보세요."
    ></textarea>
    <input type="submit" @click="onSubmit()" id="detail-review-submit" />
  </div>
</template>

<script>
import { mapActions } from "vuex";

export default {
  props: {
    id: {
      type: Number,
      default: 0
    }
  },
  data() {
    return {
      params: {
        score: 0,
        content: ""
      },
      isLogin: false
    };
  },
  async mounted() {
    const token = localStorage.getItem("token");
    if (token !== null) {
      this.isLogin = true;
    }
  },
  methods: {
    ...mapActions("detail", ["reviewWrite"]),
    ...mapActions("auth", ["isTokenVerify"]),
    textareaResize() {
      const target = document.getElementById("detail-review-textarea");
      target.style.height = "20px";
      target.style.height = 12 + target.scrollHeight + "px";
    },
    async onSubmit() {
      console.log(this.params);
      const verify = await this.isTokenVerify();
      if (verify === false) {
        alert("로그인 정보를 확인해 주세요");
        return;
      }
      const params = {
        lego_set_id: this.id,
        content: this.params["content"],
        score: this.params["score"]
      };
      await this.reviewWrite(params);
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
