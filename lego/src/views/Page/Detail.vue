<template>
  <div>
    <div id="detail-main">
      <div id="detail-imgs">
        <detail-imgs :images="model.image"></detail-imgs>
      </div>
      <div id="detail-side">
        <detail-side
          :id="model.id"
          :setName="model.name"
          :nickname="model.nickname"
          :parts="model.parts.length"
        ></detail-side>
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
      <detail-part v-if="btnFlag == 'parts'" :parts="model.parts"></detail-part>
    </div>
  </div>
</template>

<script>
import DetailImgs from "../../components/Detail/Body/DetailImgs.vue";
import DetailSide from "../../components/Detail/Body/DetailSide.vue";
import DetailReviewWrite from "../../components/Detail/Review/DetailReviewWrite.vue";
import DetailReview from "../../components/Detail/Review/DetailReview.vue";
import DetailPart from "../../components/Detail/Part/DetailPart.vue";
import { mapState, mapActions } from "vuex";

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
  computed: {
    ...mapState({
      model: state => state.detail.model
    })
  },
  async mounted() {
    const modelId = this.$route.params.modelId;
    await this.getModelDetail(modelId);
    // console.log(this.model);
  },
  methods: {
    ...mapActions("detail", ["getModelDetail"]),
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
