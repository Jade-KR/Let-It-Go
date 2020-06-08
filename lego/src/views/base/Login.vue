<template>
  <div id="login-back">
    <div id="login-body">
      <div id="login-img-box">
        <img
          src="../../assets/logo.png"
          alt=""
          id="login-img"
          @click="goHome()"
        />
      </div>
      <div @keypress.enter="onSubmit()">
        <div>
          <input
            type="text"
            id="login-id"
            placeholder="아이디"
            v-model="userInfo.id"
          />
        </div>
        <div>
          <input
            type="password"
            id="login-pwd"
            placeholder="비밀번호"
            v-model="userInfo.password"
          />
        </div>
        <button id="login-btn" @click="onSubmit()">Login</button>
      </div>
      <div id="divideLine">
        <hr
          style="width:37%; display:inline-block; margin-right:10px; border: 0.5px solid gold;"
        />
        <p style="display:inline;">또는</p>
        <hr
          style="width:37%; display:inline-block; margin-left:10px; border: 0.5px solid gold;"
        />
      </div>
      <div>
        계정이 없으신가요?
        <button style="color:gold; margin-top: 20px;" @click="goRegi()">
          가입하기
        </button>
      </div>
      <div>
        or
      </div>
      <div>
        홈으로
        <button style="color:gold;" @click="goHome()">돌아가기</button>
      </div>
    </div>
  </div>
</template>

<script>
import router from "../../router";
import { mapActions, mapMutations } from "vuex";

export default {
  data() {
    return {
      userInfo: {
        id: "",
        password: ""
      }
    };
  },
  mounted() {
    this.setAuthFlag(true);
  },
  destroyed() {
    this.setAuthFlag(false);
  },
  methods: {
    ...mapActions("auth", ["SHA256", "login"]),
    ...mapMutations("auth", ["setAuthFlag"]),
    goRegi() {
      router.push("/register");
    },
    goHome() {
      this.setAuthFlag(false);
      router.push("/");
    },
    async onSubmit() {
      let hashPwd = "";
      await this.SHA256(String(this.userInfo.password)).then(res => {
        hashPwd = res;
      });
      const params = {
        username: this.userInfo.id,
        password: hashPwd
      };
      this.login(params);
    }
  }
};
</script>

<style scoped>
#login-back {
  text-align: center;
  height: 100vh;
  width: 100%;
  background-image: url("../../assets/login_bg.jpg");
  background-position: center;
  background-repeat: no-repeat;
  background-size: cover;
}
#login-body {
  background-color: rgb(0, 0, 0);
  background-color: rgba(0, 0, 0, 0.8);
  border: 5px solid gold;
  color: white;
  width: 600px;
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  padding: 30px;
  z-index: 10;
}
#login-img-box {
  margin-bottom: 40px;
}
#login-img {
  width: 80%;
  cursor: pointer;
}
#login-id,
#login-pwd {
  border: 1px solid gold;
  color: white;
  width: 80%;
  margin-bottom: 20px;
  line-height: 40px;
  font-size: 25px;
  text-align: center;
}
#login-id::placeholder,
#login-pwd::placeholder {
  color: white;
}
#login-id:hover,
#login-pwd:hover {
  background-color: orange;
}
#login-btn,
#login-kakao {
  background-color: red;
  color: gold;
  width: 80%;
  line-height: 40px;
  font-size: 25px;
  font-weight: 800;
  padding: 5px;
  margin-bottom: 20px;
}
#login-btn:hover {
  background-color: skyblue;
  color: white;
}
#login-kakao {
  margin-top: 20px;
  background-color: gold;
  color: black;
}
#login-kakao:hover {
  background-color: skyblue;
  color: white;
}
@media screen and (max-width: 600px) {
  #login-body {
    width: 100%;
  }
}
</style>
