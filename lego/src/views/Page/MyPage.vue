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
          <hr id="divied_line" v-if="currentState === 2" />
          <div v-if="currentState === 2" class="sub_menu">
            <div
              class="fas fa-scroll sub_menu_tab"
              @click="setSubState(1)"
              :style="subState === 1 ? btnStyle[0] : btnStyle[1]"
            >
              설계도
            </div>
            <div
              class="fas fa-cubes sub_menu_tab2"
              @click="setSubState(2)"
              :style="subState === 2 ? btnStyle[0] : btnStyle[1]"
            >
              부품
            </div>
          </div>
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
        <Inventory v-if="currentState === 2 && subState === 1"></Inventory>
        <Parts v-if="currentState === 2 && subState === 2"></Parts>
      </div>
    </div>
  </div>
</template>

<script>
import MyPageHeader from "@/components/MyPage/MyPageHeader/MyPageHeader.vue";
import Models from "@/components/MyPage/MyPageBody/Model/Models.vue";
import Like from "@/components/MyPage/MyPageBody/Like/Like.vue";
import Parts from "@/components/MyPage/MyPageBody/Part/Parts.vue";
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
        { title: "보관함", icon: "fas fa-archive" }
      ],
      currentState: 0,
      subState: 1,
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
    setSubState(value) {
      const bodyContainer = document.querySelector(".body");
      bodyContainer.classList.add("anim-out");
      setTimeout(() => {
        this.subState = value;
        bodyContainer.classList.remove("anim-out");
      }, 300);
    },
    menuState(title, idx) {
      const bodyContainer = document.querySelector(".body");
      bodyContainer.classList.add("anim-out");
      setTimeout(() => {
        this.currentState = idx;
        this.btnFlag = title;
        bodyContainer.classList.remove("anim-out");
      }, 300);
    }
  }
};
</script>

<style scoped>
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
  min-height: 50px;
  height: 100%;
  margin-bottom: 10px;
  margin-top: 10px;
  justify-content: center;
}
.menu {
  font-size: 17px;
  color: rgb(160, 159, 159);
  margin-right: 100px;
  width: 6vw;
  margin-top: 10px;
}
#menu2 {
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
.sub_menu {
  display: flex;
  justify-content: center;
  margin-top: 20px;
  margin-bottom: 20px;
}
.sub_menu_tab,
.sub_menu_tab2 {
  font-size: 17px;
  color: rgb(160, 159, 159);
  margin-right: 100px;
  width: 6vw;
  cursor: pointer;
}
.sub_menu_tab:hover,
.sub_menu_tab2:hover {
  color: black;
  font-weight: bold;
}
.sub_menu_tab2 {
  margin-right: 0;
}
#divied_line {
  border: 1px dashed gold;
  width: 80%;
  margin: auto;
  margin-top: 20px;
}
@media screen and (max-width: 600px) {
  .whole_box {
    width: 100%;
  }
  .header {
    margin-bottom: 0px;
    height: 100%;
  }
  .menu {
    width: 100px;
    margin: 0px;
    margin-right: 10px;
  }
  .body_menu_bar {
    margin-bottom: 0;
  }
  .body {
    height: 100%;
    margin-bottom: 40px;
  }
  .sub_menu {
    margin-top: 10px;
    margin-bottom: 10px;
  }
  .sub_menu_tab,
  .sub_menu_tab2 {
    width: 80px;
    margin: 0px;
    margin-right: 40px;
  }
  .sub_menu_tab2 {
    margin-right: 0;
  }
  #divied_line {
    margin-top: 10px;
  }
}
</style>
