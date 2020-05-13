<template>
  <div>
    <div class="container">
      <div class="left_menu_box">
        <div class="menu_box" v-for="(menu, idx) in menus" :key="menu">
          <p :id="`menu${idx}`" @click="menuState(idx, menus.length)">{{menu}}</p>
        </div>
      </div>
      <div class="right_body_box"></div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      menus: ["프로필 편집", "비밀번호 변경", "분류기 설정"],
      currentState: 0
    };
  },
  methods: {
    menuState(idx, n) {
      this.currentState = idx;
      for (let i = 0; i < n; i++) {
        let target = document.getElementById(`menu${i}`);
        i === idx
          ? (target.style.fontWeight = "bold")
          : (target.style.fontWeight = "normal");
      }
    }
  }
};
</script>

<style scoped>
.container {
  border: 1px rgb(247, 153, 31) solid;
  width: 55%;
  height: 100%;
  display: flex;
  padding: 0;
  margin-top: 30px;
}
.left_menu_box {
  border: 1px rgb(247, 153, 31) solid;
  width: 25%;
  height: 500px;
  background: green;
}
.right_body_box {
  border: 1px rgb(247, 153, 31) solid;
  width: 75%;
  background: orange;
}
.menu_box {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 60px;
}
.menu_box > p {
  margin: 0;
  width: 80%;
  height: 100%;
  padding-top: 20px;
}
.menu_box:hover {
  transition-duration: 0.4s;
  transition: ease-in;
  cursor: pointer;
}
</style>