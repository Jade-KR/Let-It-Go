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
            <b>{{ nickname }}</b>
          </div>
          <div id="detail_side_designer_id" @click="goOfficial()" v-else>
            <b>{{ nickname }}</b>
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
            <b>{{ themeName }}</b>
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
              <b>#{{ tag }}</b>
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
            {{ likeCount }}
          </div>
        </div>
        <button id="detail_side_onlikes" @click="pushLike()" v-else>
          <i class="fas fa-heart" />
        </button>
      </div>

      <hr class="divide_line" />

      <div id="detail_side_similar">
        <div id="detail_side_similar_text">You Can Make</div>
        <div id="detail_side_similar_percent">{{ makePercent }}%</div>
      </div>
    </div>
    <div id="detail_side_ad">
      <div id="detail_side_content">레고레일로 분류를 해보세요!</div>
    </div>
  </div>
</template>

<script>
import LegoThemes from "../../../../jsonData/LegoThemes.json";
import router from "../../../router";
import { mapActions } from "vuex";

export default {
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
      makePercent: ""
    };
  },
  watch: {
    async tags() {
      if (this.tags) {
        this.tagList = await this.tags.split("|");
      }
    },
    theme() {
      this.themeName = this.legoThemeList[this.theme - 1][2];
    },
    isLike() {
      if (this.isLike === 1) {
        this.likeFlag = true;
      } else if (this.isLike === 0) {
        this.likeFlag = false;
      }
    }
  },
  async mounted() {
    if (this.tags) {
      this.tagList = await this.tags.split("|");
    }
    this.themeName = this.legoThemeList[this.theme - 1][2];
    if (this.isLike === 1) {
      this.likeFlag = true;
    } else if (this.isLike === 0) {
      this.likeFlag = false;
    }

    const myparts = await this.getUserPartsAll();
    var allPartSum = 0;
    const sortedParts = Object();
    this.parts.forEach(e => {
      let part_id = e.part_id;
      let color_id = e.color_id;
      let quantity = e.quantity;
      allPartSum += quantity;
      let temp = Object();
      temp[color_id] = quantity;
      sortedParts[part_id] = temp;
    });

    var myPartSum = 0;
    for (let i = 0; i < myparts.length; ++i) {
      if (sortedParts[myparts[i].part_id]) {
        if (sortedParts[myparts[i].part_id][myparts[i].color_id]) {
          if (
            sortedParts[myparts[i].part_id][myparts[i].color_id] >=
            myparts[i].quantity
          ) {
            myPartSum += myparts[i].quantity;
          } else {
            myPartSum += sortedParts[myparts[i].part_id][myparts[i].color_id];
          }
        }
      }
    }
    this.makePercent = ((myPartSum / allPartSum) * 100).toFixed(1);
    if (this.makePercent === "100.0") {
      this.makePercent = "100";
    }
  },
  methods: {
    ...mapActions("detail", ["onLike", "getUserPartsAll"]),
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
      const params = {
        set_id: this.id
      };
      const setLike = await this.onLike(params);
      if (setLike === "좋아요") {
        this.likeFlag = true;
      } else if (setLike === "좋아요 취소") {
        this.likeFlag = false;
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
#detail_side_similar_text {
  font-size: 28px;
}
#detail_side_similar_percent {
  font-size: 64px;
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
</style>
