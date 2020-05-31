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
            <follower-card
              :image="follower.image"
              :isFollow="follower.isFollow"
              :id="follower.id"
              :nickname="follower.nickname"
              :idx="i"
            ></follower-card>
          </div>
        </div>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
import FollowerCard from "./FollowerCard";
import { mapState, mapActions } from "vuex";

export default {
  components: {
    FollowerCard
  },
  props: {
    followerList: {
      type: Array
    }
  },
  data() {
    return {
      follower: false,
      followFlag: false
    };
  },
  computed: {
    ...mapState({
      myFollowingList: state => state.mypage.myFollowingList
    })
  },
  watch: {
    follower() {
      for (let i = 0; i < this.followerList.length; ++i) {
        if (this.followerList[i]["id"] === Number(localStorage.getItem("pk"))) {
          this.followerList[i]["isFollow"] = "me";
          continue;
        }
        this.followerList[i]["isFollow"] = "false";
        for (let j = 0; j < this.myFollowingList.length; ++j) {
          if (this.myFollowingList[j]["id"] === this.followerList[i]["id"]) {
            this.followerList[i]["isFollow"] = "true";
          }
        }
      }
    }
  },
  methods: {
    ...mapActions("mypage", ["onFollowInModal"]),
    close() {
      this.follower = false;
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
