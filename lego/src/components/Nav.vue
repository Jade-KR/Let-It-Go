<template>
  <div>
    <div class="nav">
      <div class="nav_left">
        <div class="logo_box" @click="goHome">
          <img src="../assets/logo.png" alt />
        </div>
      </div>
      <div class="nav_middle">
        <div class="menu">NEW!</div>
        <div class="menu">POP!</div>
        <div class="menu">CAN!</div>
      </div>
      <div class="nav_right">
        <div class="icons_box" v-if="login">
          <i class="fas fa-home" @click="goHome"></i>
          <i class="fas fa-search"></i>
          <i class="fas fa-user-alt" @click="goMyPage"></i>
        </div>
        <div class="icons_box" v-else>
          <button @click="goLogin">로그인</button>
          <button @click="goSignUp">회원가입</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      login: 1
    };
  },
  methods: {
    goMyPage() {
      this.$router.push("/MyPage");
    },
    goHome() {
      this.$router.push("/");
    },
    goLogin() {
      this.$router.push("/login");
    },
    goSignUp() {
      this.$router.push("/register");
    }
  }
};
</script>

<style scoped>
.nav {
  display: flex;
  justify-content: space-between;
  width: 100%;
  height: fit-content;
  border-bottom: rgb(255, 213, 26) solid 4px;
  position: fixed;
  z-index: 1;
  background: white;
}
.nav_left {
  width: 100%;
}
.logo_box {
  position: relative;
  left: 20px;
  width: 250px;
  height: 90px;
}
.logo_box:hover {
  cursor: pointer;
}
.logo_box > img {
  width: 90%;
  position: relative;
  left: 12px;
  top: 5px;
}
.nav_middle {
  width: 100%;
  display: flex;
  justify-content: space-around;
  align-items: center;
}
.menu {
  font-size: 30px;
  margin-right: 20px;
}
.nav_right {
  display: flex;
  justify-content: flex-end;
  width: 100%;
  align-items: center;
}
.icons_box {
  position: relative;
  right: 50px;
  display: flex;
  justify-content: flex-end;
  width: 300px;
}
.icons_box > i {
  font-size: 30px;
  margin-right: 20px;
}
.icons_box > i:hover {
  cursor: pointer;
}
.icons_box > button:nth-child(1) {
  width: 66px;
  height: 35px;
  margin-right: 20px;
  color: white;
  background: rgb(138, 211, 89);
  border-radius: 15%;
}
.icons_box > button:nth-child(2) {
  width: 66px;
  height: 35px;
  margin-right: 20px;
  color: rgb(138, 211, 89);
  font: bolder;
}
</style>