<template>
  <div>
    <v-dialog v-model="following" width="30vw">
      <template v-slot:activator="{ on }">
        <div v-on="on"><slot name="following" /></div>
      </template>
      <v-card class="follow" color="white">
        <div class="follow_header">
          팔로우
          <i class="fas fa-times follow_header_close" @click="close()"></i>
        </div>
        <div class="follow_body">
          <div v-for="(following, i) in followingList" :key="`following-${i}`">
            <div class="follow_card">
              <img
                :src="following.image"
                alt="user_image"
                class="follow_card_img"
                v-if="following.image !== 'null'"
                @click="goYourPage(following.id)"
              />
              <img
                src="../../../../public/images/user.png"
                alt="no_img"
                class="follow_card_img"
                v-else
                @click="goYourPage(following.id)"
              />
              <div
                class="follow_card_nickname"
                @click="goYourPage(following.id)"
              >
                {{ following.nickname }}
              </div>
              <div
                class="follow_card_btn"
                v-if="following.isFollow === false"
                @click="pushFollow(i, following.id)"
              >
                팔로우
              </div>
              <div
                class="follow_card_btn"
                v-else-if="following.isFollow === true"
                @click="pushFollow(i, following.id)"
              >
                팔로우취소
              </div>
              <div
                class="follow_card_btn"
                v-else
                @click="pushFollow(i, following.id)"
              >
                It's Me
              </div>
            </div>
          </div>
        </div>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
import { mapState, mapActions } from "vuex";
import router from "../../../router";

export default {
  props: {
    followingList: {
      type: Array
    }
  },
  data() {
    return {
      following: false,
      followFlag: false
    };
  },
  computed: {
    ...mapState({
      myFollowingList: state => state.mypage.myFollowingList
    })
  },
  watch: {
    following() {
      for (let i = 0; i < this.followingList.length; ++i) {
        if (
          this.followingList[i]["id"] === Number(localStorage.getItem("pk"))
        ) {
          this.followingList[i]["isFollow"] = "me";
          continue;
        }
        this.followingList[i]["isFollow"] = false;
        for (let j = 0; j < this.myFollowingList.length; ++j) {
          if (this.myFollowingList[j]["id"] === this.followingList[i]["id"]) {
            this.followingList[i]["isFollow"] = true;
          }
        }
      }
    }
  },
  methods: {
    ...mapActions("mypage", ["onFollowInModal"]),
    close() {
      this.following = false;
    },
    goYourPage(value) {
      router.push("/mypage/" + value);
    },
    async pushFollow(idx, user_id) {
      const params = {
        user_id: user_id
      };
      const result = await this.onFollowInModal(params);
      console.log(result);
      if (result === "팔로우") {
        this.followingList[idx]["isFollow"] = true;
        console.log(this.followingList);
      } else if (result === "팔로우 취소") {
        this.followingList[idx]["isFollow"] = false;
        console.log(this.followingList);
      } else {
        alert("문제가 발생했습니다.");
      }
    }
  }
};
</script>

<style scoped>
.follow_header {
  text-align: center;
  font-size: 20px;
  padding: 10px;
  font-weight: 600;
  color: gray;
  border-bottom: 1px solid gold;
  position: sticky;
  top: 0px;
  background-color: white;
}
.follow_header_close {
  float: right;
  cursor: pointer;
  font-size: 24px;
}
.follow_body {
  padding: 10px;
}
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
</style>
