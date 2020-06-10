<template>
  <div>
    <div class="nav" v-if="isMobile === false">
      <div class="nav_left">
        <div class="logo_box" @click="goHome()">
          <img src="@/assets/logo.png" alt id="logo_box_img" />
        </div>
      </div>
      <div class="nav_middle">
        <button class="button" id="nav_new" @click="onHomeCate(1)">
          <span data-title="최신순!">NEW!</span>
        </button>
        <button class="button" id="nav_pop" @click="onHomeCate(2)">
          <span data-title="인기도순!">POP!</span>
        </button>
        <button
          class="button"
          id="nav_you"
          @click="onHomeCate(3)"
          v-if="checkLogin === true"
        >
          <span data-title="추천순!">YOU!</span>
        </button>
      </div>
      <div class="nav_right">
        <div class="icons_box">
          <i class="fas fa-search right_icon" @click="goSearch"></i>
          <i
            class="fas fa-plus right_icon"
            @click="goWrite"
            v-if="checkLogin === true"
          ></i>
          <div class="mypage" @click="goMyPage" v-show="checkLogin">
            <img
              :src="profilePic"
              alt="noImage"
              class="picture"
              id="right_img"
            />
          </div>
          <span
            class="login_btn logRegi"
            v-if="checkLogin === false"
            @click="goLogin()"
            >로그인</span
          >
          <span
            class="register_btn logRegi"
            v-if="checkLogin === false"
            @click="goRegister()"
            >회원가입</span
          >
        </div>
      </div>
    </div>

    <div v-else>
      <div id="nav_mobile_top">
        <div class="logo_box" @click="goHome()">
          <img src="@/assets/logo.png" alt id="logo_box_img" />
        </div>
        <button class="button" id="nav_new" @click="onHomeCate(1)">
          <span data-title="새로운">NEW!</span>
        </button>
        <button class="button" id="nav_pop" @click="onHomeCate(2)">
          <span data-title="인기도">POP!</span>
        </button>
        <button
          class="button"
          id="nav_you"
          @click="onHomeCate(3)"
          v-if="checkLogin === true"
        >
          <span data-title="추천">YOU!</span>
        </button>
      </div>
      <div class="nav">
        <div class="nav_right">
          <div class="icons_box">
            <i class="fas fa-home" @click="goHome"></i>
            <i class="fas fa-search right_icon" @click="goSearch"></i>
            <div class="mypage" @click="goMyPage" v-show="checkLogin">
              <img
                :src="profilePic"
                alt="noImage"
                class="picture"
                id="right_img"
              />
            </div>
            <span
              class="login_btn logRegi"
              v-if="checkLogin === false"
              @click="goLogin()"
              >로그인</span
            >
          </div>
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
        localStorage.getItem("image") != "null" || ""
          ? localStorage.getItem("image")
          : require("@/../public/images/user.png"),
      checkLogin: localStorage.getItem("token") != null ? true : false,
      isMobile: false
    };
  },
  computed: {
    ...mapState({
      photoFlag: state => state.user.photoFlag
    })
  },
  watch: {
    photoFlag() {
      const tmp =
        localStorage.getItem("image") == "null" || ""
          ? require("@/../public/images/user.png")
          : localStorage.getItem("image");
      this.profilePic = tmp;
    }
  },
  created() {
    window.addEventListener("scroll", this.scrollEvent);
  },
  beforeDestroy() {
    window.removeEventListener("scroll", this.scrollEvent);
    window.removeEventListener("resize", this.onResponsiveInverted);
  },
  mounted() {
    this.onResponsiveInverted();
    window.addEventListener("resize", this.onResponsiveInverted);
  },
  methods: {
    ...mapActions("auth", ["isTokenVerify", "logout", "login", "register"]),
    ...mapMutations("home", ["setHomeCate"]),
    onResponsiveInverted() {
      if (window.outerWidth <= 600) {
        this.isMobile = true;
      } else {
        this.isMobile = false;
      }
    },
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
    goMember() {
      window.scrollTo(0, 0);
      router.push("/member");
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
      if (window.outerWidth >= 600) {
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
            const logRegi = document.getElementsByClassName("logRegi");
            logRegi.forEach(e => {
              e.style.fontSize = "12px";
            });
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
          const logRegi = document.getElementsByClassName("logRegi");
          logRegi.forEach(e => {
            e.style.fontSize = "16px";
          });
        }
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
  /* margin-left: 20px; */
}
.register_btn {
  width: 66px;
  height: 35px;
  /* margin-right: 20px; */
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
#nav_you span:after {
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

@media screen and (max-width: 600px) {
  #nav_mobile_top {
    position: fixed;
    top: 0;
    z-index: 20;
    display: flex;
    width: 100%;
    background-color: white;
    justify-content: space-between;
    box-shadow: 0 2px 2px gray;
  }
  .nav {
    position: fixed;
    bottom: 0;
    padding: 0px;
    box-shadow: 0 -2px 2px gray;
    border-bottom: none;
  }
  .logo_box {
    transform: translateY(4px);
    padding-left: 10px;
    margin-right: 10px;
  }
  .logo_box > img {
    width: 100px;
  }
  .nav_right {
    display: block;
  }
  .icons_box {
    display: flex;
    justify-content: space-between;
    transform: unset;
    padding: 10px 30px;
  }
  .icons_box > i {
    font-size: 30px;
  }
  .login_btn {
    transform: translateY(0px);
    font-size: 20px;
    width: 100px;
    border-radius: 15px;
    margin-right: 0px;
  }

  .button {
    width: 100%;
    font-size: 20px;
    padding: 2px;
  }
  .mypage {
    width: 30px;
    height: 30px;
  }
}
</style>
