<template>
  <div id="regi-back">
    <div id="regi-body">
      <div id="regi-img-box">
        <img src="../../assets/logo.png" alt id="regi-img" @click="goHome()" />
      </div>
      <div>
        혹시 이미 가입하셨나요?
      </div>
      <div>
        로그인하러
        <button style="color:gold; margin-bottom: 20px;" @click="goLogin()">
          돌아가기
        </button>
      </div>

      <div v-if="!loading">
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
              <span v-show="errors" class="error_box">{{ errors[0] }}</span>
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
                v-model="userInfo.password1"
              />
              <br />
              <span v-if="errors" class="error_box">{{ errors[0] }}</span>
            </div>
          </ValidationProvider>

          <ValidationProvider
            name="비밀번호 확인"
            rules="required|confirmed:pwd_confirmation"
          >
            <div slot-scope="{ errors }" style="margin-bottom: 20px;">
              <input
                type="password"
                id="regi-pwd2"
                placeholder="비밀번호 확인"
                v-model="userInfo.password2"
              />
              <br />
              <span v-if="errors" class="error_box">{{ errors[0] }}</span>
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
              <span v-if="errors" class="error_box">{{ errors[0] }}</span>
            </div>
          </ValidationProvider>

          <ValidationProvider name="나이" rules="required">
            <div
              slot-scope="{ errors }"
              style="margin-bottom: 20px;"
              id="regi-age-box"
            >
              <input
                type="number"
                step="1"
                min="1"
                max="80"
                id="regi-age"
                placeholder="나이"
                v-model="userInfo.age"
              />
              <div class="regi-gender-label" @click="selectGender(0)" id="male">
                남
              </div>
              <div
                class="regi-gender-label"
                @click="selectGender(1)"
                id="female"
              >
                여
              </div>
              <br />
              <span v-if="errors" class="error_box">{{ errors[0] }}</span>
            </div>
          </ValidationProvider>

          <ValidationProvider name="닉네임" rules="required|nickname|max:12">
            <div slot-scope="{ errors }" style="margin-bottom: 20px;">
              <input
                type="text"
                id="regi-nickname"
                placeholder="닉네임"
                v-model="userInfo.nickname"
              />
              <div id="regi-random-nick" @click="randomNick()">Random</div>
              <br />
              <span v-if="errors" class="error_box">{{ errors[0] }}</span>
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
      <div v-else>
        <button class="buttonload">
          <i class="fa fa-spinner fa-spin" id="loading"></i>
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import router from "../../router";
import { ValidationProvider, ValidationObserver } from "vee-validate";
import { mapActions, mapMutations } from "vuex";

export default {
  components: {
    ValidationProvider,
    ValidationObserver
  },
  data() {
    return {
      loading: false,
      userInfo: {
        username: "",
        password1: "",
        password2: "",
        email: "",
        nickname: "",
        age: "",
        gender: -1
      },
      randomNickNoun: [
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
      ],
      randomNickAdj: [
        "빛나는",
        "멋있는",
        "맛있는",
        "시크한",
        "아름다운",
        "강렬한",
        "강력한",
        "상큼한",
        "예쁜",
        "귀여운",
        "막막한"
      ],
      randomNickAdv: [
        "빨갛게",
        "노랗게",
        "파랗게",
        "검게",
        "하얗게",
        "둥글게",
        "각지게",
        "네모나게",
        "붉게"
      ]
    };
  },
  mounted() {
    this.setAuthFlag(true);
    this.userInfo.gender = -1;
  },
  destroyed() {
    this.setAuthFlag(false);
  },
  methods: {
    ...mapActions("auth", ["SHA256", "register"]),
    ...mapMutations("auth", ["setAuthFlag"]),
    setHash(pwd) {
      this.SHA256(pwd);
    },
    async onSubmit() {
      if (this.userInfo.gender === -1) {
        alert("성별을 선택해 주세요");
        return;
      }
      if (this.userInfo.age > 80 || this.userInfo.age < 0) {
        alert("혹시 신선이신가요..? 나이를 확인해주세요");
        return;
      }
      this.loading = true;
      let hashPwd = "";
      await this.SHA256(String(this.userInfo.password1)).then(res => {
        hashPwd = res;
      });
      const params = {
        username: this.userInfo.username,
        password1: hashPwd,
        password2: hashPwd,
        email: this.userInfo.email,
        nickname: this.userInfo.nickname,
        image: "null",
        comment: "null",
        age: this.userInfo.age,
        gender: this.userInfo.gender
      };
      const result = await this.register(params);
      if (result === false) {
        this.loading = false;
      }
    },
    goLogin() {
      router.push("/login");
    },
    goHome() {
      this.setAuthFlag(false);
      router.push("/");
    },
    randomNick() {
      const randomNumNoun = Math.floor(
        Math.random() * this.randomNickNoun.length
      );
      const randomNumAdj = Math.floor(
        Math.random() * this.randomNickAdj.length
      );
      const randomNumAdv = Math.floor(
        Math.random() * this.randomNickAdv.length
      );
      this.userInfo.nickname =
        this.randomNickAdv[randomNumAdv] +
        this.randomNickAdj[randomNumAdj] +
        this.randomNickNoun[randomNumNoun];
    },
    selectGender(value) {
      this.userInfo.gender = value;
      if (value === 0) {
        document.getElementById("male").style.backgroundColor = "blue";
        document.getElementById("female").style.backgroundColor = "";
      } else {
        document.getElementById("female").style.backgroundColor = "blue";
        document.getElementById("male").style.backgroundColor = "";
      }
    }
  }
};
</script>

<style scoped>
#regi-back {
  text-align: center;
  height: 100vh;
  width: 100%;
  background-image: url("../../assets/login_bg.jpg");
  background-position: center;
  background-repeat: no-repeat;
  background-size: cover;
}
#regi-body {
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
#regi-img-box {
  margin-bottom: 10px;
}
#regi-img {
  width: 80%;
  cursor: pointer;
}
.error_box {
  width: 100%;
  position: absolute;
  color: red;
  background-color: unset;
  right: 50%;
  transform: translateX(50%);
}
#regi-id,
#regi-pwd,
#regi-pwd2,
#regi-email,
#regi-age,
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
#regi-pwd2::placeholder,
#regi-email::placeholder,
#regi-age::placeholder,
#regi-nickname::placeholder {
  color: white;
}
#regi-id:focus {
  background-color: red;
}
#regi-pwd:focus {
  background-color: orange;
}
#regi-pwd2:focus {
  background-color: gold;
}
#regi-email:focus {
  background-color: green;
}
#regi-age:focus {
  background-color: blue;
}
#regi-nickname:focus {
  background-color: navy;
}
#regi-id:hover {
  background-color: red;
}
#regi-pwd:hover {
  background-color: orange;
}
#regi-pwd2:hover {
  background-color: gold;
}
#regi-email:hover {
  background-color: green;
}
#regi-age:hover {
  background-color: blue;
}
#regi-nickname:hover {
  background-color: navy;
}
#regi-nickname {
  width: 60%;
}
#regi-random-nick {
  cursor: pointer;
  display: inline-block;
  background-color: rgba(255, 215, 0, 0.7);
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
#loading {
  font-size: 50px;
  margin: 50px auto;
}
#regi-age {
  width: 50%;
}
.regi-gender-label {
  cursor: pointer;
  display: inline-block;
  background-color: rgba(255, 215, 0, 0.7);
  color: white;
  line-height: 40px;
  font-size: 25px;
  text-align: center;
  width: 15%;
  border: 1px solid gold;
}
.regi-gender-label:hover {
  background-color: blue;
}
.regi-gender-label:focus {
  background-color: blue;
}
@media screen and (max-width: 600px) {
  #regi-body {
    width: 100%;
  }
  #regi-random-nick {
    font-size: 16px;
    transform: translateY(-3.5px);
    /* cursor: pointer;
    display: inline-block;
    background-color: rgba(255, 215, 0, 0.7);
    color: white;
    line-height: 40px;
    font-size: 25px;
    text-align: center;
    width: 20%;
    border: 1px solid gold; */
  }
}
</style>
