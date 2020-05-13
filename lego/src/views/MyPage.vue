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
          @click.prevent="menuState(idx, menus.length)"
          :id="`menu${idx}`"
          v-for="(menu,idx) in menus"
          :key="`first${idx}`"
        >
          <i :class="menu.icon"></i>
          {{menu.title}}
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
      currentState: 0
    };
  },
  mounted() {
    let target = document.getElementById(`menu${this.currentState}`);
    target.style.fontWeight = "bold";
    target.style.color = "black";
  },
  methods: {
    menuState(idx, n) {
      this.currentState = idx;
      for (let i = 0; i < n; i++) {
        let target = document.getElementById(`menu${i}`);
        if (i === idx) {
          target.style.fontWeight = "bold";
          target.style.color = "black";
        } else {
          target.style.fontWeight = "normal";
          target.style.color = "rgb(160, 159, 159)";
        }
      }
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
