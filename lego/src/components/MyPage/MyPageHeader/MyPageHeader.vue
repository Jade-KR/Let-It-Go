<template>
  <div>
    <div class="whole_box">
      <div class="my_photo">
        <div class="photo_box">
          <img
            src="../../../../public/images/user.png"
            alt="no_image"
            v-if="image == null || image == '' || image == 'null'"
          />
          <img :src="`${image}`" alt="user_image" v-else />
        </div>
      </div>
      <div class="my_info">
        <div class="info_top">
          <span class="user_id">{{ nickname }}</span>
          <div v-if="!isMe" class="user_follow" @click="pushFollow()">
            <div v-if="followFlag">팔로우 취소</div>
            <div v-else>팔로우</div>
          </div>
          <UserModal v-else>
            <span class="user_setting" slot="click">
              <i class="fas fa-cog"></i>
            </span>
          </UserModal>
        </div>
        <div class="info_middle">
          <div class="summary">
            <span>설계도 {{ modelCnt }}</span>
          </div>
          <div class="summary cursor">
            <follower :followerList="followerList">
              <span slot="follower">팔로워 {{ followerList.length }}</span>
            </follower>
          </div>
          <div class="summary cursor">
            <following :followingList="followingList">
              <span slot="following">팔로우 {{ followingList.length }}</span>
            </following>
          </div>
        </div>
        <div class="info_bottom" v-if="comment === 'null'">
          레고를 안 산 사람은 있어도, 하나만 산 사람은 없다.
          <br />레고와 함께라면 놀이가 교육이다. <br />무엇을 생각하는가? 일단
          지르고 고민해라. <br />레고는 아름답고, 쌓을만한 가치가 있다.
        </div>
        <div class="info_bottom" v-else>
          <div v-for="(comment, i) in comments" :key="`comm-${i}`">
            {{ comment }}
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import UserModal from "../UserModal";
import Follower from "./Follower/Follower";
import Following from "./Following/Following";
import { mapState, mapActions } from "vuex";

export default {
  components: {
    UserModal,
    Follower,
    Following
  },
  props: {
    id: {
      type: Number,
      default: 0
    },
    image: {
      type: String,
      default: ""
    },
    nickname: {
      type: String,
      default: ""
    },
    comment: {
      type: String,
      default: ""
    },
    legoSet: {
      type: Number,
      default: 0
    }
  },
  data() {
    return {
      isMe: true,
      followFlag: true,
      modelCnt: 0,
      comments: []
    };
  },
  async mounted() {
    const params = {
      page: 1,
      append: false,
      id: this.$route.params.user_id
    };
    const resp = await this.checkModelsCnt(params);
    this.modelCnt = resp.data.count;
    this.comments = this.comment.split("\n");
  },
  computed: {
    ...mapState({
      followingList: state => state.mypage.followingList,
      followerList: state => state.mypage.followerList
    })
  },
  watch: {
    async id() {
      await this.follower(this.id);
      await this.following(this.id);
      const userPK = Number(localStorage.getItem("pk"));
      if (this.id !== userPK) {
        this.isMe = false;
      } else if (this.id === userPK) {
        this.isMe = true;
      }
    },
    followerList() {
      if (this.followerList.length === 0) {
        this.followFlag = false;
        return;
      }
      for (let i = 0; i < this.followerList.length; ++i) {
        if (this.followerList[i].id === Number(localStorage.getItem("pk"))) {
          this.followFlag = true;
          return;
        }
        this.followFlag = false;
      }
    },
    comment() {
      this.comments = this.comment.split("\n");
    }
  },
  methods: {
    ...mapActions("mypage", [
      "onFollow",
      "follower",
      "following",
      "checkModelsCnt"
    ]),
    async pushFollow() {
      const params = {
        user_id: this.$route.params.user_id
      };
      const result = await this.onFollow(params);
      if (result === "팔로우") {
        this.followFlag = true;
      } else if (result === "팔로우 취소") {
        this.followFlag = false;
      } else {
        alert("문제가 발생했습니다.");
      }
    }
  }
};
</script>

<style scoped>
.whole_box {
  display: flex;
  flex-flow: row nowrap;
  border-style: none;
  width: 100%;
  height: 200px;
  margin-top: 30px;
}
.my_photo {
  border-style: none;
  height: 100%;
  width: 30%;
  margin-right: 30px;
}
.my_info {
  border-style: none;
  width: 70%;
  height: fit-content;
}
.info_top {
  border-style: none;
  height: auto;
  margin-bottom: 20px;
  display: flex;
  align-items: baseline;
}
.info_middle {
  display: flex;
  border-style: none;
  height: auto;
  margin-bottom: 20px;
}
.info_bottom {
  border-style: none;
  height: 100px;
  width: 100%;
  overflow: hidden;
  text-overflow: ellipsis;
}
.photo_box {
  border-style: none;
  height: 100%;
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
}
.photo_box > img {
  width: 70%;
  height: 100%;
  border-radius: 180%;
}
.user_id {
  font-size: 30px;
  margin-right: 10px;
}
.summary {
  margin-right: 20px;
}
.user_setting:hover {
  cursor: pointer;
}
.user_setting > i {
  font-size: 25px;
}
.user_follow {
  padding: 5px 10px;
  background-color: gold;
  font-weight: 700;
  border-radius: 10px;
  transform: translateY(-5px);
  cursor: pointer;
}
.cursor {
  cursor: pointer;
}
@media screen and (max-width: 600px) {
  .whole_box {
    display: block;
    padding: 5px 10px 0 10px;
    margin-top: 20px;
    height: 100%;
  }
  .my_photo {
    height: 70px;
    width: 70px;
    display: inline-block;
    position: absolute;
    top: 60px;
    left: 20px;
  }
  .photo_box > img {
    width: 70px;
    height: 70px;
  }
  .my_info {
    display: inline-block;
    width: 100%;
  }
  .user_id {
    font-size: 18px;
  }
  .info_middle {
    margin: 30px 0 30px 100px;
  }
  .info_bottom {
    height: 100%;
  }
  .user_follow {
    font-size: 12px;
    transform: translateY(-3px);
    padding: 3px 6px;
  }
}
</style>
