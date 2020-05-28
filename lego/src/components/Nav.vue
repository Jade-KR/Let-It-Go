<template>
  <div>
    <div class="nav">
      <div class="nav_left">
        <div class="logo_box" @click="goHome">
          <img src="@/assets/logo.png" alt />
        </div>
      </div>
      <div class="nav_middle">
        <button class="button" id="nav_new" @click="onHomeCate(1)">
          <span data-title="새로운거!">NEW!</span>
        </button>
        <button class="button" id="nav_pop" @click="onHomeCate(2)">
          <span data-title="인기도순!">POP!</span>
        </button>
      </div>
      <div class="nav_right">
        <div class="icons_box">
          <i class="fas fa-search" @click="goSearch"></i>
          <i class="fas fa-plus" @click="goWrite"></i>
          <div class="mypage" @click="goMyPage" v-show="checkLogin">
            <img :src="profilePic" alt="noImage" class="picture" />
          </div>
          <span class="login_btn" v-if="checkLogin === false" @click="goLogin()">로그인</span>
          <span class="register_btn" v-if="checkLogin === false" @click="goRegister()">회원가입</span>
          <!-- <i class="fas fa-user-alt" @click="goMyPage"></i> -->
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { mapActions, mapMutations, mapState } from "vuex";
import router from "../router";

export default {
  data() {
    return {
      profilePic:
        localStorage.getItem("image") != "null"
          ? localStorage.getItem("image")
          : require("@/../public/images/user.png"),
      checkLogin: localStorage.getItem("token") != null ? true : false
    };
  },
  computed: {
    ...mapState({
      photoFlag: state => state.user.photoFlag
    })
  },
  watch: {
    photoFlag() {
      this.profilePic = localStorage.getItem("image");
    }
  },
  methods: {
    ...mapActions("auth", ["isTokenVerify", "logout", "login", "register"]),
    ...mapMutations("home", ["setHomeCate"]),
    async goMyPage() {
      const isVerify = await this.isTokenVerify();
      if (isVerify === false) {
        return;
      }
      const locationNow = location.pathname;
      const user_id = localStorage.getItem("pk");
      if (locationNow !== "/mypage/" + user_id) {
        this.$router.push("/mypage" + "/" + user_id);
      }
    },
    goSearch() {
      const locationNow = location.pathname;
      if (locationNow !== "/search") {
        this.$router.push("/search");
      }
    },
    goLogin() {
      this.$router.push("/login");
    },
    goRegister() {
      this.$router.push("/register");
    },
    goHome() {
      const locationNow = location.pathname;
      if (locationNow !== "/") {
        this.$router.push("/");
      }
    },
    async goWrite() {
      const isVerify = await this.isTokenVerify();
      if (isVerify === false) {
        return;
      }
      const locationNow = location.pathname;
      if (locationNow !== "/write") {
        this.$router.push("/write");
      }
    },
    async onHomeCate(value) {
      await this.setHomeCate(value);
      const locationLength = location.origin.length + 1;
      const locationNow = location.href.length;
      if (locationLength !== locationNow) {
        router.push("/");
      }
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
  z-index: 10;
  background: white;
  padding: 10px 12vw;
}
.nav_left {
  width: 100%;
}
.logo_box {
  height: 70px;
}
.logo_box:hover {
  cursor: pointer;
}
.logo_box > img {
  width: 230px;
}
.nav_middle {
  width: 100%;
  display: flex;
  justify-content: space-around;
  align-items: center;
}
.nav_right {
  display: flex;
  justify-content: flex-end;
  width: 100%;
  align-items: center;
}
.icons_box {
  display: flex;
  justify-content: flex-end;
  transform: translateY(5px);
}
.icons_box > i {
  font-size: 30px;
  margin-right: 20px;
}
.icons_box > i:hover {
  cursor: pointer;
}
.login_btn {
  width: 66px;
  height: 35px;
  margin-right: 20px;
  color: white;
  background: rgb(138, 211, 89);
  border-radius: 15%;
  text-align: center;
  line-height: 35px;
  font-weight: bold;
  cursor: pointer;
  transform: translateY(-4px);
  margin-left: 20px;
}
.register_btn {
  width: 66px;
  height: 35px;
  margin-right: 20px;
  color: rgb(138, 211, 89);
  text-align: center;
  line-height: 35px;
  font-weight: bold;
  cursor: pointer;
  transform: translateY(-4px);
}

.button {
  display: inline-block;
  overflow: hidden;
  width: 12vw;
  perspective: 400px;
  background-color: transparent;
  font-size: 30px;
}
.button span {
  display: block;
  position: relative;
  transition: 0.3s ease-in-out all;
  transform-origin: 50% 0;
  transform-style: preserve-3d;
  background-color: white;
  color: black;
  width: 100%;
}
.button span:after {
  display: block;
  content: attr(data-title);
  position: absolute;
  left: 0;
  top: 0;
  transition: 0.3s ease-in-out all;
  transform-origin: 50% 0;
  transform: translate3d(0px, 105%, 0px) rotateX(-90deg);
  background-color: black;
  color: white;
  width: 100%;
}
#nav_new span:after {
  background-color: gold;
}
#nav_pop span:after {
  background-color: green;
}
#nav_can span:after {
  background-color: red;
}
.button:hover span {
  transform: translate3d(0px, 0px, -30px) rotateX(90deg);
}
.mypage {
  width: 33px;
  height: 33px;
  border-radius: 50%;
  cursor: pointer;
  transform: translateY(-3px);
}
.picture {
  width: 100%;
  height: 100%;
  border-radius: 50%;
}
</style>
