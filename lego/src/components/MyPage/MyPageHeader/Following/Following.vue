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
            <following-card
              :image="following.image"
              :isFollow="following.isFollow"
              :id="following.id"
              :nickname="following.nickname"
              :idx="i"
            ></following-card>
          </div>
        </div>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
import FollowingCard from "./FollowingCard";
import { mapState, mapActions } from "vuex";

export default {
  components: {
    FollowingCard
  },
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
        this.followingList[i]["isFollow"] = "false";
        for (let j = 0; j < this.myFollowingList.length; ++j) {
          if (this.myFollowingList[j]["id"] === this.followingList[i]["id"]) {
            this.followingList[i]["isFollow"] = "true";
          }
        }
      }
    }
  },
  methods: {
    ...mapActions("mypage", ["onFollowInModal"]),
    close() {
      this.following = false;
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
