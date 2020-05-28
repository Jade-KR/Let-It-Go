<template>
  <div>
    <div id="detail_side_box">
      <div id="detail_side_desc">
        <div id="detail_side_title">
          <!-- <b>WHATISTHISWHATIST HISWHATISTHI SWHATISTHISWHATISTHIS</b> -->
          <b>{{ setName }}</b>
        </div>

        <hr class="divide_line" />

        <div id="detail_side_designers">
          <div id="detail_side_designer">Designer</div>
          <div id="detail_side_designer_id" @click="goMypage()">
            <b>{{ nickname }}</b>
          </div>
        </div>
        <div id="detail_side_bricks">
          <div id="detail_side_brick">Bricks</div>
          <div id="detail_side_part">
            <b>{{ parts }} Parts</b>
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
          <div id="detail_side_score">Score</div>
          <div id="detail_side_score_num">5.0</div>
        </div>
        <div id="detail_side_likes" @click="pushLike()" v-if="likeFlag === false">
          <div id="detail_side_like">Like</div>
          <div id="detail_side_like_num">12</div>
        </div>
        <button id="detail_side_onlikes" @click="pushLike()" v-else>
          <i class="fas fa-heart" />
        </button>
      </div>

      <hr class="divide_line" />

      <div id="detail_side_similar">
        <div id="detail_side_similar_text">You Can Make</div>
        <div id="detail_side_similar_percent">86%</div>
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
    parts: {
      type: Number,
      default: 0
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
    }
  },
  data() {
    return {
      tagList: ["태그가 없습니다."],
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
      ]
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
  },
  methods: {
    ...mapActions("detail", ["onLike"]),
    goMypage() {
      if (this.userId === null) {
        var user_id = localStorage.getItem("pk");
      } else {
        user_id = this.userId;
      }
      router.push("/mypage" + "/" + user_id);
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
  /* border: 1px solid black; */
  /* background-color: rgba(255, 215, 0, 0.6); */
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
