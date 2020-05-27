<template>
  <div>
    <v-dialog v-model="follower" width="30vw">
      <template v-slot:activator="{ on }">
        <div v-on="on"><slot name="follower" /></div>
      </template>
      <v-card class="follow" color="white">
        <div class="follow_header">
          팔로워
          <i class="fas fa-times follow_header_close" @click="close()"></i>
        </div>
        <div class="follow_body">
          <div v-for="(follower, i) in followerList" :key="`follower-${i}`">
            <div class="follow_card">
              <img
                :src="follower.image"
                alt="user_image"
                class="follow_card_img"
                v-if="follower.image !== 'null'"
                @click="goYourPage(follower.id)"
              />
              <img
                src="../../../../public/images/user.png"
                alt="no_img"
                class="follow_card_img"
                v-else
                @click="goYourPage(follower.id)"
              />
              <div
                class="follow_card_nickname"
                @click="goYourPage(follower.id)"
              >
                {{ follower.nickname }}
              </div>
              <div class="follow_card_btn">
                팔로우
              </div>
            </div>
          </div>
        </div>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
import router from "../../../router";
export default {
  props: {
    followerList: {
      type: Array
    }
  },
  data() {
    return {
      follower: false
    };
  },
  methods: {
    close() {
      this.follower = false;
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
}
</style>
