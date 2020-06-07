<template>
  <div>
    <div id="detail_side_box">
      <div id="detail_side_desc">
        <div id="detail_side_title">
          <b>{{ setName }}</b>
        </div>

        <hr class="divide_line" />

        <div id="detail_side_designers">
          <div id="detail_side_designer">Designer</div>
          <div
            id="detail_side_designer_id"
            @click="goMypage()"
            v-if="nickname !== 'Official Set'"
          >
            <b class="fontColor_green">{{ nickname }}</b>
          </div>
          <div id="detail_side_designer_id" @click="goOfficial()" v-else>
            <b class="fontColor_green">{{ nickname }}</b>
          </div>
        </div>
        <div id="detail_side_bricks">
          <div id="detail_side_brick">Bricks</div>
          <div id="detail_side_part">
            <b>{{ partsLength }} Parts</b>
          </div>
        </div>
        <div id="detail_side_themes">
          <div id="detail_side_theme">Theme</div>
          <div id="detail_side_theme_name">
            <b class="fontColor_green" @click="searchTheme(theme)">{{
              themeName
            }}</b>
          </div>
        </div>
        <div id="detail_side_tags">
          <div id="detail_side_tag">Tags</div>
          <div id="detail_side_taglist">
            <div
              v-for="(tag, i) in tagList"
              :key="`tag-${i}`"
              style="display: inline-block; margin-right: 10px;"
            >
              <b class="fontColor_green" @click="searchTag(tag)">#{{ tag }}</b>
            </div>
          </div>
        </div>
      </div>

      <hr class="divide_line" />

      <div id="detail_side_number">
        <div id="detail_side_scores">
          <div id="detail_side_score">
            Score
          </div>
          <div id="detail_side_score_num">
            {{ avgScore }}
          </div>
        </div>
        <div
          id="detail_side_likes"
          @click="pushLike()"
          v-if="likeFlag === false"
        >
          <div id="detail_side_like">
            Like
          </div>
          <div id="detail_side_like_num">
            {{ likeCnt }}
          </div>
        </div>
        <button id="detail_side_onlikes" @click="pushLike()" v-else>
          <i class="fas fa-heart">
            <div id="detail_side_like_num_on">
              {{ likeCnt }}
            </div>
          </i>
        </button>
      </div>

      <hr class="divide_line" />

      <div id="detail_side_similar">
        <div v-if="isInven" id="detail_side_similar_inven">
          설계도를 보관중입니다.
        </div>
        <div>
          <div id="detail_side_similar_text">You Can Make</div>
          <div id="detail_side_similar_percent">{{ makePercent }}%</div>
        </div>

        <add-inven
          id="detail_side_similar_add"
          v-if="is100 === true"
          @addInven="addModelToInven()"
        >
          <div slot="add_inven">
            보관함에 설계도 추가하기
          </div>
        </add-inven>

        <sub-inven
          id="detail_side_similar_sub"
          v-if="isInven === true"
          @subInven="subModelToInven()"
        >
          <div slot="sub_inven">
            보관함에서 설계도 제거하기
          </div>
        </sub-inven>
      </div>
    </div>
    <video
      controls
      autoplay
      width="100%"
      style="margin-top: 10px;"
      @click="goFood()"
    >
      <source src="../../../assets/food_curation.mp4" type="video/mp4" />
    </video>
  </div>
</template>

<script>
import AddInven from "./ConfirmModal/AddInven.vue";
import SubInven from "./ConfirmModal/SubInven.vue";
import LegoThemes from "../../../../jsonData/LegoThemes.json";
import router from "../../../router";
import { mapActions, mapState } from "vuex";

export default {
  components: {
    AddInven,
    SubInven
  },
  props: {
    id: {
      type: Number,
      default: 0
    },
    setName: {
      type: String,
      default: ""
    },
    nickname: {
      type: String,
      default: ""
    },
    partsLength: {
      type: Number,
      default: 0
    },
    parts: {
      type: Array
    },
    tags: {
      type: String,
      default: ""
    },
    theme: {
      type: Number,
      default: 1
    },
    userId: {
      type: Number,
      default: 0
    },
    isLike: {
      type: Number,
      default: -1
    },
    likeCount: {
      type: Number,
      default: 0
    },
    avgScore: {
      type: Number,
      default: 0
    },
    setQuantity: {
      type: Number,
      default: 0
    }
  },
  data() {
    return {
      tagList: [],
      themeName: "",
      legoThemeList: LegoThemes["rows"],
      likeFlag: false,
      followFlag: false,
      checked: [
        {
          backgroundColor: "red",
          color: "white"
        }
      ],
      unchecked: [
        {
          backgroundColor: "rgba(0,0,0,0)",
          color: "black"
        }
      ],
      makePercent: "0.0",
      likeCnt: 0,
      is100: false,
      preprocedParts: [],
      isInven: false
    };
  },
  watch: {
    makePercent() {
      if (this.makePercent === "100") {
        this.is100 = true;
      }
    },
    async tags() {
      if (this.tags) {
        this.tagList = await this.tags.split("|");
      }
    },
    isLike() {
      if (this.isLike === 1) {
        this.likeFlag = true;
      } else if (this.isLike === 0) {
        this.likeFlag = false;
      }
    },
    myparts() {
      if (this.myparts === undefined) {
        this.myparts = [];
        this.makePercent = "0.0";
        return;
      }
      if (this.parts.length === 0) {
        this.makePercent = "0.0";
        return;
      }
      const partsObj = Object();
      this.parts.forEach(e => {
        let temp = `${e.part_id}_${e.color_id}`;
        if (partsObj[temp]) {
          partsObj[temp]["quantity"] += e.quantity;
        } else {
          partsObj[temp] = {
            color_id: e.color_id,
            part_id: e.part_id,
            quantity: e.quantity
          };
        }
      });
      this.preprocedParts = [];
      for (let i in partsObj) {
        this.preprocedParts.push(partsObj[i]);
      }
      var allPartSum = 0;
      const sortedParts = Object();
      this.preprocedParts.forEach(e => {
        let part_id = e.part_id;
        let color_id = e.color_id;
        let quantity = e.quantity;
        allPartSum += quantity;
        let temp = Object();
        temp[color_id] = quantity;
        sortedParts[`${part_id}_${color_id}`] = temp;
      });
      var myPartSum = 0;
      for (let i = 0; i < this.myparts.length; ++i) {
        if (
          sortedParts[`${this.myparts[i].part_id}_${this.myparts[i].color_id}`]
        ) {
          if (
            sortedParts[
              `${this.myparts[i].part_id}_${this.myparts[i].color_id}`
            ][this.myparts[i].color_id]
          ) {
            if (
              sortedParts[
                `${this.myparts[i].part_id}_${this.myparts[i].color_id}`
              ][this.myparts[i].color_id] >= this.myparts[i].quantity
            ) {
              myPartSum += this.myparts[i].quantity;
            } else {
              myPartSum +=
                sortedParts[
                  `${this.myparts[i].part_id}_${this.myparts[i].color_id}`
                ][this.myparts[i].color_id];
            }
          }
        }
      }
      this.makePercent = ((myPartSum / allPartSum) * 100).toFixed(1);
      if (this.makePercent === "100.0") {
        this.makePercent = "100";
      }
    }
  },
  computed: {
    ...mapState({
      myparts: state => state.detail.myparts
    })
  },
  async mounted() {
    await this.getUserPartsAll();
    if (this.tags) {
      this.tagList = await this.tags.split("|");
    }
    var temp = "";
    for (let i = 0; i < this.legoThemeList.length; ++i) {
      if (Number(this.legoThemeList[i][0]) === Number(this.theme)) {
        temp = this.legoThemeList[i][2];
      }
    }
    this.themeName = temp;
    if (this.isLike === 1) {
      this.likeFlag = true;
    } else if (this.isLike === 0) {
      this.likeFlag = false;
    }
    this.likeCnt = this.likeCount;
    if (this.setQuantity >= 1) {
      this.isInven = true;
    }
  },
  methods: {
    ...mapActions("detail", [
      "onLike",
      "getUserPartsAll",
      "addInven",
      "subInven"
    ]),
    ...mapActions("search", ["searchByDetail"]),
    goMypage() {
      if (this.userId === null) {
        var user_id = localStorage.getItem("pk");
      } else {
        user_id = this.userId;
      }
      router.push("/mypage" + "/" + user_id);
    },
    goOfficial() {
      window.open("https://www.lego.com/ko-kr");
    },
    async pushLike() {
      if (!localStorage.getItem("pk")) {
        alert("로그인 후 사용해 주세요");
        return;
      }
      const params = {
        set_id: this.id
      };
      const setLike = await this.onLike(params);
      if (setLike === "좋아요") {
        this.likeFlag = true;
        if (this.isLike === 1) {
          this.likeCnt = this.likeCount;
        } else {
          this.likeCnt = this.likeCount + 1;
        }
      } else if (setLike === "좋아요 취소") {
        this.likeFlag = false;
        if (this.isLike === 1) {
          this.likeCnt = this.likeCount - 1;
        } else {
          this.likeCnt = this.likeCount;
        }
      } else {
        alert("문제가 발생했습니다.");
      }
    },
    isFollow() {
      if (this.followFlag === false) {
        this.followFlag = true;
      } else {
        this.followFlag = false;
      }
    },
    async addModelToInven() {
      const params = {
        add_set: Number(this.id)
      };
      const result = await this.addInven(params);
      if (result === "갱신 완료") {
        alert("보관함에 저장되었습니다.");
        location.reload();
      } else {
        alert("문제가 생겼습니다.");
      }
    },
    async subModelToInven() {
      const params = {
        sub_set: Number(this.id)
      };
      const result = await this.subInven(params);
      if (result === "갱신 완료") {
        alert("보관함에서 삭제되었습니다.");
        location.reload();
      } else {
        alert("문제가 생겼습니다.");
      }
    },
    async searchTheme(value) {
      const params = {
        type: "theme",
        word: value
      };
      await this.searchByDetail(params);
      router.push("/search");
    },
    async searchTag(value) {
      const params = {
        type: "tag",
        word: value
      };
      await this.searchByDetail(params);
      router.push("/search");
    },
    goFood() {
      window.open("https://i02d106.p.ssafy.io/");
    }
  }
};
</script>

<style scoped>
#detail_side_box {
  border: 3px solid gold;
  padding: 10px;
}
.divide_line {
  border: 1px solid gold;
  margin: 20px 0;
}
#detail_side_desc {
  text-align: center;
  overflow: hidden;
}
#detail_side_title {
  font-size: 24px;
  margin-top: 20px;
  margin-bottom: 10px;
}
#detail_side_designers,
#detail_side_bricks,
#detail_side_themes,
#detail_side_tags {
  display: flex;
  text-align: start;
}
#detail_side_designer,
#detail_side_brick,
#detail_side_theme,
#detail_side_tag {
  width: 90px;
  padding: 5px 0;
  font-size: 18px;
}
#detail_side_designer_id,
#detail_side_part,
#detail_side_theme_name,
#detail_side_taglist {
  width: 200px;
  padding: 5px 0 5px 10px;
  /* text-align: start; */
}
#detail_side_designer_id {
  cursor: pointer;
}
#detail_side_number {
  display: flex;
}
#detail_side_scores,
#detail_side_likes {
  width: 50%;
  border: 1px solid green;
  margin: 10px;
  text-align: center;
}
#detail_side_score,
#detail_side_like {
  font-size: 20px;
}
#detail_side_score_num,
#detail_side_like_num {
  font-size: 40px;
}
#detail_side_similar {
  text-align: center;
}
#detail_side_similar_inven {
  font-size: 20px;
  background-color: green;
  padding: 3px;
  color: white;
  font-weight: 700;
}
#detail_side_similar_text {
  font-size: 28px;
}
#detail_side_similar_percent {
  font-size: 64px;
}
#detail_side_similar_add {
  font-size: 20px;
  background-color: gold;
  padding: 3px;
  color: white;
  font-weight: 700;
  cursor: pointer;
}
#detail_side_similar_add:hover {
  background-color: green;
}
#detail_side_similar_add:hover::after {
  content: "보관함에 설계도를 추가하고 해당 설계도에 사용된 부품을 내 부품에서 삭제합니다.";
  color: gold;
  font-size: 18px;
  width: 250px;
  position: absolute;
  transform: translate(-50%, 0%);
  border: 1px solid black;
  background-color: white;
  padding: 5px;
}
#detail_side_similar_sub {
  font-size: 20px;
  background-color: red;
  padding: 3px;
  color: white;
  font-weight: 700;
  cursor: pointer;
}
#detail_side_similar_sub:hover {
  background-color: green;
}
#detail_side_similar_sub:hover::after {
  content: "보관함에서 설계도를 제거하고 해당 설계도에 사용된 부품을 내 부품에 추가합니다.";
  color: red;
  font-size: 18px;
  width: 250px;
  position: absolute;
  transform: translate(-50%, 0%);
  border: 1px solid black;
  background-color: white;
  padding: 5px;
}
#detail_side_likes {
  cursor: pointer;
  transition: 0.5s;
}
#detail_side_onlikes {
  width: 50%;
  cursor: pointer;
  font-size: 80px;
  color: red;
}
#detail_side_likes:hover {
  background-color: red;
  color: white;
}

#detail_side_ad {
  margin-top: 10px;
  background-color: rgba(255, 215, 0, 0.6);
  height: 200px;
  text-align: center;
  padding: 20px;
}
#detail_side_content {
  font-size: 24px;
  vertical-align: middle;
}
#detail_side_like_num_on {
  color: white;
  text-align: center;
  position: absolute;
  transform: translate(-10%, -200%);
  font-size: 30px;
  width: 100px;
}
.fontColor_green {
  color: green;
  cursor: pointer;
  font-weight: 400;
}
@media screen and (max-width: 600px) {
  #detail_side_box {
    border: 1px solid gold;
  }
  .divide_line {
    border: 0.1px solid gold;
  }
}
</style>
