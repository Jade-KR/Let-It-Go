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
            :partsLength="model.parts.length"
            :parts="model.parts"
            :tags="model.tags"
            :theme="model.theme"
            :userId="model.user_id"
            :isLike="model.is_like"
            :likeCount="model.like_count"
            :avgScore="avgScore"
            :setQuantity="model.set_quantity"
          ></detail-side>
        </div>
      </div>
      <div id="detail_desc">
        <detail-desc :description="model.description"></detail-desc>
      </div>
      <div id="detail_recommend">
        <div id="detail_recommend_header">이런 설계도는 어떠세요?</div>
        <div id="detail_rec_cards">
          <div
            v-for="(v, i) in pickedList"
            :key="`recc-${i}`"
            class="detail_rec_card"
          >
            <detail-rec-card
              :id="recommendList[v].id"
              :name="recommendList[v].name"
              :images="recommendList[v].images"
              :nickname="recommendList[v].nickname"
              :isLike="recommendList[v].is_like"
              :isReview="recommendList[v].is_review"
              :likeCount="recommendList[v].like_count"
              :reviewCount="recommendList[v].review_count"
            ></detail-rec-card>
          </div>
        </div>
      </div>
      <div id="detail_btns">
        <div
          class="detail_btn"
          :style="btnFlag == 'reviews' ? btnStyle[0] : btnStyle[1]"
          @click="onReviews()"
        >
          <i class="fas fa-font"></i>&nbsp; 댓글
          <div style="display: inline-block; transform: translateY(-2px);">
            ({{ reviews.length }})
          </div>
        </div>
        <div
          class="detail_btn"
          :style="btnFlag == 'parts' ? btnStyle[0] : btnStyle[1]"
          @click="onParts()"
        >
          <i class="fas fa-cubes"></i>&nbsp; 부품
        </div>
        <div
          class="detail_btn"
          :style="btnFlag == 'Mocs' ? btnStyle[0] : btnStyle[1]"
          @click="onMocs()"
        >
          <i class="fas fa-scroll"></i>&nbsp; 하위
        </div>
      </div>
      <div id="detail_reviews">
        <div v-if="btnFlag == 'reviews'">
          <detail-review-write :id="model.id"></detail-review-write>
          <div
            v-for="(review, i) in slicedReviews"
            :key="`review-${i}`"
            id="test"
          >
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
          <v-layout justify-center>
            <v-flex xs8>
              <v-card-text>
                <v-pagination
                  :length="pageLength"
                  v-model="page"
                  color="rgb(255, 215, 0)"
                ></v-pagination>
              </v-card-text>
            </v-flex>
          </v-layout>
        </div>
        <detail-part
          v-if="btnFlag == 'parts'"
          :parts="model.parts"
          :setName="model.name"
        ></detail-part>
        <sub-set-card
          v-if="btnFlag === 'Mocs'"
          :subSets="model.sub_sets"
        ></sub-set-card>
      </div>
    </div>
    <div v-else>
      <div id="loading">
        <!-- <i class="fa fa-spinner fa-spin"></i> -->
        <div class="loadingio-spinner-bean-eater-rstzjzfll3r">
          <div class="ldio-upeca3v4hi">
            <div>
              <div></div>
              <div></div>
              <div></div>
            </div>
            <div>
              <div></div>
              <div></div>
              <div></div>
            </div>
          </div>
        </div>
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
import DetailRecCard from "../../components/Detail/Recommend/DetailRecCard.vue";
import SubSetCard from "../../components/Detail/SubSet/SubSetCard.vue";
import { mapState, mapActions, mapMutations } from "vuex";

export default {
  components: {
    DetailImgs,
    DetailDesc,
    DetailSide,
    DetailReviewWrite,
    DetailReview,
    DetailPart,
    DetailRecCard,
    SubSetCard
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
      avgScore: 0,
      pickedList: [],
      page: 1,
      pageLength: 1,
      slicedReviews: []
    };
  },
  computed: {
    ...mapState({
      model: state => state.detail.model,
      reviews: state => state.detail.reviews,
      recommendList: state => state.detail.recommendList
    }),
    start: function() {
      return this.page - 1;
    }
  },
  watch: {
    reviews() {
      this.reviewList = this.reviews;
      this.pageLength = Math.ceil(this.reviews.length / 10);
      this.slicedReviews = this.reviews.slice(this.start * 10, this.page * 10);
      var scoreSum = 0;
      this.reviewList.forEach(e => {
        scoreSum += e.score;
      });
      this.avgScore = Number((scoreSum / this.reviewList.length).toFixed(1));
      if (isNaN(this.avgScore)) {
        this.avgScore = 0;
      }
    },
    recommendList() {
      while (this.pickedList.length !== 4) {
        const randomNum = Math.floor(Math.random() * this.recommendList.length);
        var flag = false;
        for (let i = 0; i < this.pickedList.length; ++i) {
          if (this.pickedList[i] === randomNum) {
            flag = true;
          }
        }
        if (flag === false) {
          this.pickedList.push(randomNum);
        }
      }
    },
    start() {
      this.slicedReviews = [];
      setTimeout(() => {
        this.slicedReviews = this.reviews.slice(
          this.start * 10,
          this.page * 10
        );
      }, 300);
    }
  },
  beforeDestroy() {
    this.resetModel();
    this.resetMyParts();
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
    await this.getModelsByItemBased(modelId);
    this.pageLength = Math.ceil(this.reviews.length / 10);
    this.slicedReviews = this.reviews.slice(this.start * 10, this.page * 10);
    this.loading = false;
  },
  methods: {
    ...mapActions("detail", ["getModelDetail", "getModelsByItemBased"]),
    ...mapMutations("detail", ["resetModel", "resetMyParts"]),
    onReviews() {
      this.btnFlag = "reviews";
    },
    onParts() {
      this.btnFlag = "parts";
    },
    onMocs() {
      this.btnFlag = "Mocs";
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
  padding: 0 10px;
}
#detail_side {
  width: 300px;
}
#detail_desc {
  width: 1000px;
  margin: 10px auto;
  border: 3px solid gold;
  padding: 30px;
}
#detail_recommend {
  width: 1000px;
  margin: auto;
  margin-top: 20px;
  border: 3px solid gold;
  padding: 10px 5px;
}
#detail_rec_cards {
  display: flex;
}
#detail_recommend_header {
  text-align: center;
  font-size: 22px;
  font-weight: 600;
  width: 80%;
  margin: auto;
  margin-bottom: 20px;
  border-bottom: 3px dashed gold;
  padding-bottom: 5px;
}
.detail_rec_card {
  flex: 1;
  margin: 0 5px;
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
  margin: 0 100px;
  transition: 0.5s;
  line-height: 40px;
}
.detail_btn:hover {
  color: black;
  opacity: 1;
}
#detail_reviews {
  border: 3px solid gold;
  padding: 30px;
  width: 1000px;
  margin: 10px auto;
  /* border: 1px solid gold; */
}
#loading {
  text-align: center;
  margin-top: 200px;
  font-size: 100px;
}
@media screen and (max-width: 600px) {
  #detail_main {
    width: 100%;
    display: block;
  }
  #detail_imgs {
    width: 100vw;
    height: 100%;
  }
  #detail_side {
    width: 100%;
  }
  #detail_desc {
    width: 100%;
    margin: 0px;
    padding: 10px;
    border: 1px solid gold;
  }
  #detail_recommend {
    width: 100%;
    padding-bottom: 0;
    margin-top: 5px;
    border: 1px solid gold;
  }
  #detail_rec_cards {
    display: inline-block;
    text-align: center;
  }
  #detail_recommend_header {
    margin-bottom: 0;
    border-bottom: none;
  }
  .detail_rec_card {
    flex: none;
    margin: 0px;
    display: inline-block;
  }
  #detail_btns {
    width: 100%;
    margin: 5px auto;
    display: flex;
    border-top: 1px solid gold;
    border-bottom: 1px solid gold;
  }
  .detail_btn {
    margin: 0;
    flex: 1;
  }
  #detail_reviews {
    width: 100%;
    padding: 5px;
    border: 1px solid gold;
  }
}
</style>
