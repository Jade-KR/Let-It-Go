<template>
  <div>
    <div class="bg">
      <div class="whole_box">
        <div class="left_menu_box">
          <div class="menu_box" v-for="(menu, idx) in menus" :key="menu">
            <p
              :id="`menu${idx}`"
              @click="menuState(menu, idx)"
              :style="btnFlag === menu ? btnStyle[0] : btnStyle[1]"
            >{{menu}}</p>
          </div>
        </div>
        <SetProfile v-if="currentState === 0"></SetProfile>
        <SetPassword v-if="currentState === 1"></SetPassword>
      </div>
    </div>
  </div>
</template>

<script>
import SetProfile from "../components/UserSetting/SetProfile";
import SetPassword from "../components/UserSetting/SetPassword";
export default {
  props: { title: String, idx: Number },
  components: {
    SetProfile,
    SetPassword
  },
  data() {
    return {
      menus: ["프로필 편집", "비밀번호 변경", "분류기 설정"],
      currentState: 0,
      btnFlag: "프로필 편집",
      btnStyle: [
        {
          fontWeight: "bold"
        },
        {
          fontWeight: "normal"
        }
      ]
    };
  },
  mounted() {
    this.menuState(this.title, this.idx);
  },
  methods: {
    menuState(title, idx) {
      this.currentState = idx;
      this.btnFlag = title;
      // this.currentState = idx;
      // for (let i = 0; i < n; i++) {
      //   let target = document.getElementById(`menu${i}`);
      //   i === idx
      //     ? (target.style.fontWeight = "bold")
      //     : (target.style.fontWeight = "normal");
      // }
    }
  }
};
</script>

<style scoped>
.bg {
  text-align: center;
  height: 1000px;
  width: 100%;
  display: flex;
  justify-content: center;
  background: white;
}
.whole_box {
  border: 1px silver solid;
  width: 55%;
  height: fit-content;
  display: flex;
  padding: 0;
  position: absolute;
  margin-top: 50px;
}
.left_menu_box {
  border: 1px silver solid;
  width: 25%;
  height: 500px;
}
.right_body_box {
  border: 1px silver solid;
  width: 75%;
  height: fit-content;
}
.menu_box {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 60px;
}
.menu_box:hover {
  background: #e6e6e6;
}
.menu_box > p {
  margin: 0;
  width: 80%;
  height: 100%;
  padding-top: 20px;
  text-align: left;
}
.menu_box:hover {
  cursor: pointer;
}
</style>