<template>
  <div>
    <div class="whole_box">
      <div class="header">
        <MyPageHeader></MyPageHeader>
      </div>
      <hr />
      <div class="body_menu_bar">
        <button
          class="menu"
          @click.prevent="menuState(menu.title, idx)"
          :id="`menu${idx}`"
          v-for="(menu,idx) in menus"
          :key="`first${idx}`"
          :style="btnFlag === menu.title ? btnStyle[0] : btnStyle[1]"
        >
          <i :class="menu.icon">{{menu.title}}</i>
        </button>
      </div>
      <div class="body">
        <MyPageBody></MyPageBody>
      </div>
    </div>
  </div>
</template>

<script>
import MyPageHeader from "@/components/MyPage/MyPageHeader.vue";
import MyPageBody from "@/components/MyPage/MyPageBody.vue";
export default {
  components: {
    MyPageHeader,
    MyPageBody
  },
  data() {
    return {
      menus: [
        { title: "설계도", icon: "fas fa-scroll" },
        { title: "부품", icon: "fas fa-cubes" },
        { title: "좋아요", icon: "fas fa-heart" },
        { title: "기타", icon: "fas fa-scroll" },
        { title: "등등", icon: "fas fa-scroll" }
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
      ]
    };
  },
  mounted() {
    this.menuState("설계도", 0);
  },
  methods: {
    menuState(title, idx) {
      this.currentState = idx;
      this.btnFlag = title;
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
  margin-right: 40px;
  width: 6vw;
}
.menu:hover {
  color: black;
  font-weight: bold;
}
.body {
  border-style: none;
  height: fit-content%;
  width: 100%;
}
</style>
