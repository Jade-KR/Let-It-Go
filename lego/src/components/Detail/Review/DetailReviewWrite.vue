<template>
  <div id="detail_review_write" v-if="isLogin">
    <div class="rating">
      <i
        class="fas fa-star"
        @click="ratingUpdate(1)"
        :style="params.score <= 0 ? ratingStyle[1] : ratingStyle[0]"
      ></i>
      <i
        class="fas fa-star"
        @click="ratingUpdate(2)"
        :style="params.score <= 1 ? ratingStyle[1] : ratingStyle[0]"
      ></i>
      <i
        class="fas fa-star"
        @click="ratingUpdate(3)"
        :style="params.score <= 2 ? ratingStyle[1] : ratingStyle[0]"
      ></i>
      <i
        class="fas fa-star"
        @click="ratingUpdate(4)"
        :style="params.score <= 3 ? ratingStyle[1] : ratingStyle[0]"
      ></i>
      <i
        class="fas fa-star"
        @click="ratingUpdate(5)"
        :style="params.score <= 4 ? ratingStyle[1] : ratingStyle[0]"
      ></i>
    </div>
    <input
      type="submit"
      @click="onSubmit()"
      id="detail_review_submit"
      v-if="isMobile === true"
      value="작성!"
    />
    <textarea
      cols="75"
      rows="2"
      id="detail_review_textarea"
      @keydown="textareaResize()"
      @keyup="textareaResize()"
      v-model="params.content"
      placeholder=" 리뷰를 작성해 보세요."
    ></textarea>
    <input
      type="submit"
      @click="onSubmit()"
      id="detail_review_submit"
      v-if="isMobile === false"
      value="작성!"
    />
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
      isLogin: false,
      ratingStyle: [
        {
          color: "gold"
        },
        {
          color: "black"
        }
      ],
      isMobile: false
    };
  },
  async mounted() {
    const token = localStorage.getItem("token");
    if (token !== null) {
      this.isLogin = true;
    }
    this.onResponsiveInverted();
    window.addEventListener("resize", this.onResponsiveInverted);
  },
  beforeDestroy() {
    window.removeEventListener("resize", this.onResponsiveInverted);
  },
  methods: {
    ...mapActions("detail", ["reviewWrite"]),
    ...mapActions("auth", ["isTokenVerify"]),
    onResponsiveInverted() {
      if (window.outerWidth < 600) {
        this.isMobile = true;
      } else {
        this.isMobile = false;
      }
    },
    textareaResize() {
      const target = document.getElementById("detail_review_textarea");
      target.style.height = "20px";
      target.style.height = 12 + target.scrollHeight + "px";
    },
    async onSubmit() {
      const verify = await this.isTokenVerify();
      if (verify === false) {
        alert("로그인 정보를 확인해 주세요");
        return;
      }
      if (this.params.score === 0) {
        alert("별점을 입력해 주세요");
        return;
      }
      if (this.params.content === "") {
        alert("리뷰를 입력해 주세요");
        return;
      }
      const params = {
        lego_set_id: this.id,
        content: this.params["content"],
        score: this.params["score"]
      };
      await this.reviewWrite(params);
      this.params.score = 0;
      this.params.content = "";
    },
    ratingUpdate(value) {
      this.params.score = value;
    }
  }
};
</script>

<style scoped>
#detail_review_write {
  border: 1px solid gold;
  padding: 10px;
  display: flex;
  margin-bottom: 20px;
}
#detail_review_textarea {
  resize: vertical;
  overflow: visible;
  border: 1px solid black;
}
#detail_review_submit {
  font-size: 24px;
  text-align: center;
  width: 100px;
  height: 70px;
  background-color: gold;
}
.rating {
  font-size: 30px;
  margin-right: 5px;
}
.fas {
  margin-top: 15px;
}
@media screen and (max-width: 600px) {
  #detail_review_write {
    display: block;
  }
  #detail_review_textarea {
    width: 100%;
  }
  #detail_review_submit {
    display: inline-block;
    float: right;
    height: 35px;
    transform: translateY(5px);
  }
  .rating {
    display: inline-block;
  }
  .fas {
    margin-top: 0;
  }
}
</style>
