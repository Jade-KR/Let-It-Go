<template>
  <div id="regi-back">
    <div id="regi-body">
      <div id="regi-img-box">
        <img
          src="../../assets/logo.png"
          alt=""
          id="regi-img"
          @click="goHome()"
        />
      </div>
      <div>
        혹시 이미 가입하셨나요?
        <button style="color:gold; margin-bottom: 20px;" @click="goLogin()">
          돌아가기
        </button>
      </div>

      <ValidationObserver ref="obs" v-slot="{ invalid, validated }">
        <ValidationProvider name="아이디" rules="required|alpha_num|max:15">
          <div slot-scope="{ errors }" style="margin-bottom: 20px;">
            <input
              type="text"
              id="regi-id"
              placeholder="아이디"
              v-model="userInfo.username"
            />
            <br />
            <span v-show="errors" class="error">{{ errors[0] }}</span>
          </div>
        </ValidationProvider>

        <ValidationProvider
          name="비밀번호"
          vid="pwd_confirmation"
          rules="required|password|min:8|max:100"
        >
          <div slot-scope="{ errors }" style="margin-bottom: 20px;">
            <input
              type="password"
              id="regi-pwd"
              placeholder="비밀번호"
              v-model="userInfo.password"
            />
            <br />
            <span v-if="errors" class="error">{{ errors[0] }}</span>
          </div>
        </ValidationProvider>

        <ValidationProvider name="이메일" rules="required|email|max:50">
          <div slot-scope="{ errors }" style="margin-bottom: 20px;">
            <input
              type="text"
              id="regi-email"
              placeholder="이메일"
              v-model="userInfo.email"
            />
            <br />
            <span v-if="errors" class="error">{{ errors[0] }}</span>
          </div>
        </ValidationProvider>

        <ValidationProvider name="닉네임" rules="required|nickname">
          <div slot-scope="{ errors }" style="margin-bottom: 20px;">
            <input
              type="text"
              id="regi-nickname"
              placeholder="닉네임"
              v-model="userInfo.nickname"
            />
            <div id="regi-random-nick" @click="randomNick()">
              Random
            </div>
            <br />
            <span v-if="errors" class="error">{{ errors[0] }}</span>
          </div>
        </ValidationProvider>

        <button
          id="regi-btn"
          @click="onSubmit()"
          :disabled="invalid || !validated"
        >
          Register
        </button>
      </ValidationObserver>
    </div>
  </div>
</template>

<script>
import router from "../../router";
import { ValidationProvider, ValidationObserver } from "vee-validate";

export default {
  components: {
    ValidationProvider,
    ValidationObserver
  },
  data() {
    return {
      userInfo: {
        username: "",
        password: "",
        email: "",
        nickname: ""
      },
      randomNickname: [
        "뽀로로",
        "둘리",
        "도우너",
        "마이콜",
        "또치",
        "고길동",
        "크롱이",
        "아기상어",
        "아빠상어",
        "엄마상어",
        "타요",
        "피카츄",
        "파이리",
        "꼬부기",
        "이상해씨",
        "아구몬"
      ]
    };
  },
  methods: {
    onSubmit() {
      console.log(this.userInfo);
    },
    goLogin() {
      router.push("/login");
    },
    goHome() {
      router.push("/");
    },
    randomNick() {
      const randomNum = Math.floor(Math.random() * this.randomNickname.length);
      this.userInfo.nickname = this.randomNickname[randomNum];
    }
  }
};
</script>

<style scoped>
#regi-back {
  text-align: center;
  height: 100vh;
  width: 100%;
  /* background-color: black; */
  background-image: url("../../assets/login_bg.jpg");
  background-position: center;
  background-repeat: no-repeat;
  background-size: cover;
  /* filter: blur(8px);
  -webkit-filter: blur(8px); */
}
#regi-body {
  background-color: rgb(0, 0, 0); /* Fallback color */
  background-color: rgba(0, 0, 0, 0.8); /* Black w/opacity/see-through */
  border: 5px solid gold;
  color: white;
  width: 40vw;
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  padding: 30px;
  z-index: 10;
}
#regi-img-box {
  margin-bottom: 10px;
}
#regi-img {
  width: 80%;
  cursor: pointer;
}
.error {
  width: 100%;
  position: absolute;
  color: red;
  right: 50%;
  transform: translateX(50%);
}
#regi-id,
#regi-pwd,
#regi-email,
#regi-nickname {
  border: 1px solid gold;
  color: white;
  width: 80%;
  /* margin-bottom: 20px; */
  line-height: 40px;
  font-size: 25px;
  text-align: center;
}
#regi-id::placeholder,
#regi-pwd::placeholder,
#regi-email::placeholder,
#regi-nickname::placeholder {
  color: white;
}
#regi-id:focus {
  background-color: red;
}
#regi-pwd:focus {
  background-color: gold;
}
#regi-email:focus {
  background-color: green;
}
#regi-nickname:focus {
  background-color: blue;
}
#regi-id:hover {
  background-color: red;
}
#regi-pwd:hover {
  background-color: gold;
}
#regi-email:hover {
  background-color: green;
}
#regi-nickname:hover {
  background-color: blue;
}
#regi-nickname {
  width: 60%;
}
#regi-random-nick {
  cursor: pointer;
  display: inline-block;
  background-color: green;
  color: white;
  line-height: 40px;
  font-size: 25px;
  text-align: center;
  width: 20%;
  border: 1px solid gold;
}
#regi-random-nick:hover {
  background-color: navy;
}
#regi-btn {
  background-color: red;
  color: gold;
  width: 80%;
  line-height: 40px;
  font-size: 25px;
  font-weight: 800;
  padding: 5px;
  margin-bottom: 20px;
}
#regi-btn:enabled:hover {
  background-color: purple;
  color: white;
}
#regi-btn:disabled {
  background-color: grey;
  color: whitesmoke;
}
</style>
