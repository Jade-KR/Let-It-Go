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
    followingList: {
      type: Array
    }
  },
  data() {
    return {
      following: false
    };
  },
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
