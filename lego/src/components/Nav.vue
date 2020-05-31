<template>
  <div>
    <div class="nav">
      <div class="nav_left">
        <div class="logo_box" @click="goHome">
          <img src="@/assets/logo.png" alt id="logo_box_img" />
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
          <i class="fas fa-search right_icon" @click="goSearch"></i>
          <i class="fas fa-plus right_icon" @click="goWrite"></i>
          <div class="mypage" @click="goMyPage" v-show="checkLogin">
            <img
              :src="profilePic"
              alt="noImage"
              class="picture"
              id="right_img"
            />
          </div>
          <span
            class="login_btn right_icon"
            v-if="checkLogin === false"
            @click="goLogin()"
            >로그인</span
          >
          <span
            class="register_btn right_icon"
            v-if="checkLogin === false"
            @click="goRegister()"
            >회원가입</span
          >
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
  created() {
    window.addEventListener("scroll", this.scrollEvent);
  },
  beforeDestroy() {
    window.removeEventListener("scroll", this.scrollEvent);
  },
  methods: {
    ...mapActions("auth", ["isTokenVerify", "logout", "login", "register"]),
    ...mapMutations("home", ["setHomeCate"]),
    async goMyPage() {
      window.scrollTo(0, 0);
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
      window.scrollTo(0, 0);
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
      window.scrollTo(0, 0);
      const locationNow = location.pathname;
      if (locationNow !== "/") {
        this.$router.push("/");
      }
    },
    async goWrite() {
      window.scrollTo(0, 0);
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
      window.scrollTo(0, 0);
      await this.setHomeCate(value);
      const locationLength = location.origin.length + 1;
      const locationNow = location.href.length;
      if (locationLength !== locationNow) {
        router.push("/");
      }
    },
    scrollEvent() {
      if (document.documentElement.scrollTop >= 100) {
        document.getElementById("logo_box_img").style.width = "100px";
        document.getElementById("right_img").style.width = "25px";
        document.getElementById("right_img").style.height = "25px";
        const icons = document.getElementsByClassName("right_icon");
        icons.forEach(e => {
          e.style.fontSize = "18px";
        });
        const button = document.getElementsByClassName("button");
        button.forEach(e => {
          e.style.fontSize = "18px";
        });
      } else if (document.documentElement.scrollTop === 0) {
        document.getElementById("logo_box_img").style.width = "230px";
        document.getElementById("right_img").style.width = "33px";
        document.getElementById("right_img").style.height = "33px";
        const icons = document.getElementsByClassName("right_icon");
        icons.forEach(e => {
          e.style.fontSize = "30px";
        });
        const button = document.getElementsByClassName("button");
        button.forEach(e => {
          e.style.fontSize = "30px";
        });
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
  z-index: 20;
  background: white;
  padding: 10px 12vw;
}
.nav_left {
  width: 100%;
}
.logo_box:hover {
  cursor: pointer;
}
.logo_box > img {
  width: 230px;
  transition: 0.3s ease-in-out all;
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
  transition: 0.3s ease-in-out all;
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
  transition: 0.3s ease-in-out all;
}
</style>
