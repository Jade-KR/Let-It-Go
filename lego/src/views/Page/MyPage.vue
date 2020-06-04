<template>
  <div>
    <div class="whole_box">
      <div class="header">
        <MyPageHeader
          :id="userInfo.id"
          :image="userInfo.image"
          :nickname="userInfo.nickname"
          :comment="userInfo.comment"
        ></MyPageHeader>
      </div>
      <hr />
      <div class="body_menu_bar">
        <div v-if="check === true">
          <button
            class="menu"
            @click.prevent="menuState(menu.title, idx)"
            :id="`menu${idx}`"
            v-for="(menu, idx) in menus"
            :key="`first${idx}`"
            :style="btnFlag === menu.title ? btnStyle[0] : btnStyle[1]"
          >
            <i :class="menu.icon">&nbsp;{{ menu.title }}</i>
          </button>
        </div>
        <div v-else>
          <button
            class="menu"
            @click.prevent="menuState(`설계도`, 0)"
            :style="btnStyle[0]"
          >
            <i class="fas fa-scroll">&nbsp;설계도</i>
          </button>
        </div>
      </div>
      <div class="body">
        <Models v-if="currentState === 0"></Models>
        <Like v-if="currentState === 1"></Like>
        <Parts v-if="currentState === 2"></Parts>
        <Inventory v-if="currentState === 3"></Inventory>
      </div>
    </div>
  </div>
</template>

<script>
import MyPageHeader from "@/components/MyPage/MyPageHeader/MyPageHeader.vue";
import Models from "@/components/MyPage/MyPageBody/Model/Models.vue";
import Like from "@/components/MyPage/MyPageBody/Like/Like.vue";
import Parts from "@/components/MyPage/MyPageBody/Parts/Parts.vue";
import Inventory from "@/components/MyPage/MyPageBody/Inventory/Inventory.vue";
import { mapActions } from "vuex";
import router from "../../router";

export default {
  components: {
    MyPageHeader,
    Models,
    Like,
    Parts,
    Inventory
  },
  data() {
    return {
      menus: [
        { title: "설계도", icon: "fas fa-scroll" },
        { title: "좋아요", icon: "fas fa-heart" },
        { title: "부품", icon: "fas fa-cubes" },
        { title: "보관함", icon: "fas fa-archive" }
        // { title: "조합", icon: "fas fa-puzzle-piece" },
        // { title: "등등", icon: "fas fa-scroll" }
      ],
      currentState: 0,
      btnFlag: "설계도",
      btnStyle: [
        {
          color: "black",
          fontWeight: "bold"
        },
        {
          fontSize: "17px"
        }
      ],
      userInfo: {
        id: 0,
        image: "",
        nickname: "",
        comment: "",
        lego_sets: []
      },
      check: ""
    };
  },
  async mounted() {
    this.$route.params.user_id === localStorage.getItem("pk")
      ? (this.check = true)
      : (this.check = false);
    const params = {
      user_id: this.$route.params.user_id
    };
    const result = await this.getUserInfo(params);
    if (result === 404) {
      alert("유효하지 않은 사용자입니다.");
      router.push("/");
      return;
    }
    this.userInfo = result;
    this.menuState("설계도", 0);
    await this.myFollowing();
  },
  methods: {
    ...mapActions("mypage", ["getUserInfo", "myFollowing"]),
    menuState(title, idx) {
      const bodyContainer = document.querySelector(".body");
      bodyContainer.classList.add("anim-out");
      setTimeout(() => {
        this.currentState = idx;
        this.btnFlag = title;
        bodyContainer.classList.remove("anim-out");
      }, 300);
      // this.currentState = idx;
      // for (let i = 0; i < n; i++) {
      //   let target = document.getElementById(`menu${i}`);
      //   if (i === idx) {
      //     target.style.fontWeight = "bold";
      //     target.style.color = "black";
      //   } else {
      //     target.style.fontWeight = "normal";
      //     target.style.color = "rgb(160, 159, 159)";
      //   }
      // }
    }
  }
};
</script>

<style scoped>
/* 큰 레이아웃 */
.whole_box {
  border-style: none;
  align-items: center;
  width: 60%;
  height: fit-content;
  margin: auto;
}
.header {
  border-style: none;
  width: 100%;
  height: 200px;
  margin-bottom: 20px;
}
hr {
  border: rgb(252, 193, 85) solid 1.2px;
}
.body_menu_bar {
  display: flex;
  border-style: none;
  height: 50px;
  margin-bottom: 20px;
  margin-top: 10px;
  justify-content: center;
}
.menu {
  font-size: 17px;
  color: rgb(160, 159, 159);
  margin-right: 70px;
  width: 6vw;
}
#menu3 {
  margin-right: 0;
}
.menu:hover {
  color: black;
  font-weight: bold;
}
.body {
  border-style: none;
  height: fit-content;
  width: 100%;
  opacity: 1;
  transition: all 0.3s ease-out;
}
.body.anim-out {
  opacity: 0;
  transform: scale(0.9) translateY(40px);
}
</style>
