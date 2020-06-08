<template>
  <div class="follow_card">
    <img
      :src="image"
      alt="user_image"
      class="follow_card_img"
      v-if="image !== 'null'"
      @click="goYourPage(id)"
    />
    <img
      src="../../../../../public/images/user.png"
      alt="no_img"
      class="follow_card_img"
      v-else
      @click="goYourPage(id)"
    />
    <div class="follow_card_nickname" @click="goYourPage(id)">
      {{ nickname }}
    </div>
    <div
      class="follow_card_btn"
      v-if="followFlag === 'false'"
      @click="pushFollow(idx, id)"
    >
      팔로우
    </div>
    <div
      class="follow_card_btn"
      v-else-if="followFlag === 'true'"
      @click="pushFollow(idx, id)"
    >
      팔로우취소
    </div>
    <div class="follow_card_btn" style="cursor: default" v-else>
      It's Me
    </div>
  </div>
</template>

<script>
import router from "../../../../router";
import { mapActions } from "vuex";

export default {
  props: {
    image: {
      type: String,
      default: ""
    },
    isFollow: {
      type: String,
      default: ""
    },
    id: {
      type: Number,
      default: 0
    },
    nickname: {
      type: String,
      default: ""
    },
    idx: {
      type: Number,
      default: 0
    }
  },
  data() {
    return {
      followFlag: false
    };
  },
  mounted() {
    this.followFlag = this.isFollow;
  },
  methods: {
    ...mapActions("mypage", ["onFollowInModal"]),
    goYourPage(value) {
      router.push("/mypage/" + value);
    },
    async pushFollow(idx, user_id) {
      const params = {
        user_id: user_id
      };
      const result = await this.onFollowInModal(params);
      if (result === "팔로우") {
        this.followFlag = "true";
      } else if (result === "팔로우 취소") {
        this.followFlag = "false";
      } else {
        alert("문제가 발생했습니다.");
      }
    }
  }
};
</script>

<style scoped>
.follow_card {
  display: flex;
  margin-bottom: 5px;
}
.follow_card_img {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  margin-right: 5px;
  cursor: pointer;
}
.follow_card_nickname {
  padding: 13px 0;
  flex: 1;
  cursor: pointer;
}
.follow_card_btn {
  padding: 13px 0;
  background-color: gold;
  font-weight: 600;
  width: 100px;
  text-align: center;
  line-height: 12px;
  height: 40px;
  margin-top: 7px;
  border-radius: 10px;
  cursor: pointer;
}
@media screen and (max-width: 600px) {
  .follow_card {
  }
  .follow_card_img {
    width: 40px;
    height: 40px;
  }
  .follow_card_nickname {
    padding: 10px 0;
    font-size: 14px;
  }
  .follow_card_btn {
    height: 20px;
    padding: 4.5px 0;
    margin: 0px;
    margin-top: 10px;
    font-weight: 500;
    font-size: 14px;
  }
}
</style>
