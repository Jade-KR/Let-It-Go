<template>
  <div>
    <v-dialog v-model="follower" :width="isMobile === false ? '400px' : '95vw'">
      <template v-slot:activator="{ on }">
        <div v-on="on"><slot name="follower" /></div>
      </template>
      <v-card class="follow" color="white">
        <div class="follow_header">
          팔로워
          <i class="fas fa-times follow_header_close" @click="close()"></i>
        </div>
        <div class="follow_body" v-if="isEmpty === false">
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
        <div class="follow_body empty" v-else>
          다양한 활동으로 팔로우를 모아보세요!
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
      followFlag: false,
      isEmpty: false,
      isMobile: false
    };
  },
  computed: {
    ...mapState({
      myFollowingList: state => state.mypage.myFollowingList
    })
  },
  watch: {
    follower() {
      if (this.followerList.length === 0) {
        this.isEmpty = true;
        return;
      }
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
  mounted() {
    this.onResponsiveInverted();
    window.addEventListener("resize", this.onResponsiveInverted);
  },
  beforeDestroy() {
    window.removeEventListener("resize", this.onResponsiveInverted);
  },
  methods: {
    ...mapActions("mypage", ["onFollowInModal"]),
    close() {
      this.follower = false;
    },
    onResponsiveInverted() {
      if (window.outerWidth < 600) {
        this.isMobile = true;
      } else {
        this.isMobile = false;
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
.empty {
  text-align: center;
  padding: 40px 0;
}
</style>
