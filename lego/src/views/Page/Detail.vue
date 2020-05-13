<template>
  <div>
    <div id="detail-main">
      <div id="detail-imgs">
        <detail-imgs></detail-imgs>
      </div>
      <div id="detail-side">
        <detail-side></detail-side>
      </div>
    </div>
    <div id="detail-btns">
      <div
        class="detail-btn"
        :style="btnFlag == 'reviews' ? btnStyle[0] : btnStyle[1]"
        @click="onReviews()"
      >
        <i class="fas fa-scroll"></i>&nbsp; 댓글
      </div>
      <div
        class="detail-btn"
        :style="btnFlag == 'parts' ? btnStyle[0] : btnStyle[1]"
        @click="onParts()"
      >
        <i class="fas fa-cubes"></i>&nbsp; 부품
      </div>
    </div>
    <div id="detail-desc">
      <div v-if="btnFlag == 'reviews'">
        <detail-review-write></detail-review-write>
        <detail-review></detail-review>
      </div>
      <detail-part v-if="btnFlag == 'parts'"></detail-part>
    </div>
  </div>
</template>

<script>
import DetailImgs from "../../components/Detail/DetailImgs.vue";
import DetailSide from "../../components/Detail/DetailSide.vue";
import DetailReviewWrite from "../../components/Detail/DetailReviewWrite.vue";
import DetailReview from "../../components/Detail/DetailReview.vue";
import DetailPart from "../../components/Detail/DetailPart.vue";

export default {
  components: {
    DetailImgs,
    DetailSide,
    DetailReviewWrite,
    DetailReview,
    DetailPart
  },
  data() {
    return {
      btnFlag: "reviews",
      btnStyle: [
        {
          fontSize: "24px",
          color: "black"
        },
        {
          fontSize: "20px"
        }
      ]
    };
  },
  methods: {
    onReviews() {
      this.btnFlag = "reviews";
    },
    onParts() {
      this.btnFlag = "parts";
    }
  }
};
</script>

<style scoped>
#detail-main {
  width: 1000px;
  margin: 30px auto 0 auto;
  display: flex;
}
#detail-imgs {
  width: 700px;
  /* border: 1px solid gold; */
  padding: 10px;
}
#detail-side {
  width: 300px;
  /* border: 1px solid gold; */
}
#detail-btns {
  width: 1000px;
  margin: 20px auto 0 auto;
  border-top: 3px solid gold;
  border-bottom: 3px solid gold;
  text-align: center;
  transition: all 0.5s;
}
.detail-btn {
  display: inline-block;
  font-size: 20px;
  padding: 10px;
  color: grey;
  cursor: pointer;
  margin: 0 150px;
  transition: 0.5s;
  line-height: 40px;
}
.detail-btn:hover {
  color: black;
  opacity: 1;
}
#detail-desc {
  width: 1000px;
  margin: 10px auto;
  /* border: 1px solid gold; */
}
</style>
