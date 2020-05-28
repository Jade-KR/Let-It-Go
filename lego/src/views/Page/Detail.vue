<template>
  <div>
    <div v-if="loading === false">
      <div id="detail_main">
        <div id="detail_imgs">
          <detail-imgs :images="model.images"></detail-imgs>
        </div>
        <div id="detail_side">
          <detail-side
            :id="model.id"
            :setName="model.name"
            :nickname="model.nickname"
            :parts="model.parts.length"
            :tags="model.tags"
            :theme="model.theme"
            :userId="model.user_id"
            :isLike="model.is_like"
            :likeCount="model.like_count"
            :avgScore="avgScore"
          ></detail-side>
        </div>
      </div>
      <div id="detail_desc">
        <detail-desc :description="model.description"></detail-desc>
      </div>
      <div id="detail_btns">
        <div
          class="detail_btn"
          :style="btnFlag == 'reviews' ? btnStyle[0] : btnStyle[1]"
          @click="onReviews()"
        >
          <i class="fas fa-scroll"></i>&nbsp; 댓글
        </div>
        <div
          class="detail_btn"
          :style="btnFlag == 'parts' ? btnStyle[0] : btnStyle[1]"
          @click="onParts()"
        >
          <i class="fas fa-cubes"></i>&nbsp; 부품
        </div>
      </div>
      <div id="detail_desc">
        <div v-if="btnFlag == 'reviews'">
          <detail-review-write :id="model.id"></detail-review-write>
          <div v-for="(review, i) in reviewList" :key="`review-${i}`" id="test">
            <detail-review
              :content="review.content"
              :nickname="review.nickname"
              :score="review.score"
              :userId="review.user_id"
              :reviewId="review.id"
              :updatedAt="review.updated_at"
              :userImage="review.user_image"
              :setId="model.id"
            ></detail-review>
          </div>
        </div>
        <detail-part
          v-if="btnFlag == 'parts'"
          :parts="model.parts"
          :setName="model.name"
        ></detail-part>
      </div>
    </div>
    <div v-else>
      <div id="loading">
        <i class="fa fa-spinner fa-spin"></i>
      </div>
    </div>
  </div>
</template>

<script>
import DetailImgs from "../../components/Detail/Body/DetailImgs.vue";
import DetailDesc from "../../components/Detail/Body/DetailDesc.vue";
import DetailSide from "../../components/Detail/Body/DetailSide.vue";
import DetailReviewWrite from "../../components/Detail/Review/DetailReviewWrite.vue";
import DetailReview from "../../components/Detail/Review/DetailReview.vue";
import DetailPart from "../../components/Detail/Part/DetailPart.vue";
import { mapState, mapActions, mapMutations } from "vuex";

export default {
  components: {
    DetailImgs,
    DetailDesc,
    DetailSide,
    DetailReviewWrite,
    DetailReview,
    DetailPart
  },
  data() {
    return {
      loading: false,
      btnFlag: "reviews",
      btnStyle: [
        {
          fontSize: "24px",
          color: "black"
        },
        {
          fontSize: "20px"
        }
      ],
      reviewList: [],
      avgScore: 0
    };
  },
  computed: {
    ...mapState({
      model: state => state.detail.model,
      reviews: state => state.detail.reviews
    })
  },
  watch: {
    reviews() {
      this.reviewList = this.reviews;
      var scoreSum = 0;
      this.reviewList.forEach(e => {
        scoreSum += e.score;
      });
      this.avgScore = Number((scoreSum / this.reviewList.length).toFixed(1));
    }
  },
  beforeDestroy() {
    this.resetModel();
  },
  async mounted() {
    this.loading = true;
    const modelId = this.$route.params.modelId;
    await this.getModelDetail(modelId);
    if (this.model.review_count !== 0) {
      var scoreSum = 0;
      this.reviewList.forEach(e => {
        scoreSum += e.score;
      });
      this.avgScore = Number((scoreSum / this.model.review_count).toFixed(1));
    } else {
      this.avgScore = 0;
    }
    this.loading = false;
  },
  methods: {
    ...mapActions("detail", ["getModelDetail"]),
    ...mapMutations("detail", ["resetModel"]),
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
#detail_main {
  width: 1000px;
  margin: 30px auto 0 auto;
  display: flex;
}
#detail_imgs {
  width: 700px;
  /* border: 1px solid gold; */
  padding: 0 10px;
}
#detail_side {
  width: 300px;
  /* border: 1px solid gold; */
}
#detail_desc {
  border: 3px solid gold;
  padding: 30px;
}
#detail_btns {
  width: 1000px;
  margin: 20px auto 0 auto;
  border-top: 3px solid gold;
  border-bottom: 3px solid gold;
  text-align: center;
  transition: all 0.5s;
}
.detail_btn {
  display: inline-block;
  font-size: 20px;
  padding: 10px;
  color: grey;
  cursor: pointer;
  margin: 0 150px;
  transition: 0.5s;
  line-height: 40px;
}
.detail_btn:hover {
  color: black;
  opacity: 1;
}
#detail_desc {
  width: 1000px;
  margin: 10px auto;
  /* border: 1px solid gold; */
}
#loading {
  text-align: center;
  margin-top: 200px;
  font-size: 100px;
}
</style>
