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
              <div class="follow_card_btn" v-if="following.isFollow === false">
                팔로우
              </div>
              <div
                class="follow_card_btn"
                v-else-if="following.isFollow === true"
              >
                팔로우취소
              </div>
              <div class="follow_card_btn" v-else>
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
import { mapState } from "vuex";
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
  mounted() {},
  methods: {
    close() {
      this.following = false;
    },
    goYourPage(value) {
      router.push("/mypage/" + value);
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
  margin-bottom: 5px;
  height: 50px;
  margin-right: 5px;
}
.follow_card_img {
  display: inline-block;
  width: 50px;
  height: 50px;
  border-radius: 50%;
  cursor: pointer;
}
.follow_card_nickname {
  display: inline-block;
  cursor: pointer;
  vertical-align: middle;
}
.follow_card_btn {
  display: inline-block;
  padding: 13px 0;
  background-color: gold;
  font-weight: 600;
  width: 70px;
  text-align: center;
  float: right;
}
</style>
