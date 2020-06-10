<template>
  <div>
    <div class="bg">
      <div class="whole_box">
        <div class="left_menu_box">
          <div
            class="menu_box"
            v-for="(menu, idx) in menus"
            :key="menu"
            :style="btnFlag === menu ? boxStyle[0] : boxStyle[1]"
          >
            <p
              :id="`menu${idx}`"
              @click="menuState(menu, idx)"
              :style="btnFlag === menu ? btnStyle[0] : btnStyle[1]"
            >
              {{ menu }}
            </p>
          </div>
        </div>
        <SetProfile v-if="currentState === 0"></SetProfile>
        <SetPassword v-if="currentState === 1"></SetPassword>
        <SetLegoRail v-if="currentState === 2"></SetLegoRail>
      </div>
    </div>
  </div>
</template>

<script>
import SetProfile from "@/components/UserSetting/SetProfile";
import SetPassword from "@/components/UserSetting/SetPassword";
import SetLegoRail from "@/components/UserSetting/SetLegoRail";
export default {
  props: { title: String, idx: Number },
  components: {
    SetProfile,
    SetPassword,
    SetLegoRail
  },
  data() {
    return {
      menus: ["프로필 편집", "비밀번호 변경", "레고 마스터"],
      currentState: 0,
      btnFlag: "프로필 편집",
      btnStyle: [
        {
          fontWeight: "bold"
        },
        {
          fontWeight: "normal"
        }
      ],
      boxStyle: [{ borderLeft: "3px solid black" }]
    };
  },
  mounted() {
    this.menuState(this.title, this.idx);
  },
  methods: {
    menuState(title, idx) {
      this.currentState = idx;
      this.btnFlag = title;
    }
  }
};
</script>

<style scoped>
.bg {
  text-align: center;
  height: 100%;
  width: 100%;
  display: flex;
  justify-content: center;
}
.whole_box {
  border: 1px silver solid;
  width: 60%;
  height: fit-content;
  display: flex;
  padding: 0;
  position: absolute;
  margin-top: 50px;
}
.left_menu_box {
  border-right: 1px silver solid;
  width: 25%;
  height: 500px;
}
.menu_box {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 60px;
}
.menu_box:hover {
  background: #f8f8f8;
  border-left: silver solid 3px;
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
@media screen and (max-width: 600px) {
  .bg {
    margin-top: 20px;
  }
  .whole_box {
    margin: 0px;
    display: block;
    width: 100%;
    position: static;
    border: none;
  }
  .left_menu_box {
    width: 100%;
    height: 100%;
    border-right: none;
    border-bottom: 1px solid silver;
    display: flex;
  }
  .menu_box {
    width: 33.3%;
    height: 100%;
  }
  .menu_box > p {
    width: 100%;
    text-align: center;
    padding: 10px 0;
  }
}
</style>
