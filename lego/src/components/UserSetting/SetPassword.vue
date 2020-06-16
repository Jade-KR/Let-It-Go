<template>
  <div class="right_body_box">
    <div class="all_box">
      <div class="photo_box">
        <div class="label_box">
          <div class="photo_frame">
            <img :src="profilePic" alt class="photo" />
          </div>
        </div>
        <div class="input_box">
          <div class="photo_desc">
            <h1 class="user_id">{{ name }}</h1>
          </div>
        </div>
      </div>
      <ValidationObserver ref="obs" v-slot="{ invalid, validated }">
        <div class="form_box">
          <div class="label_box">
            <p class="label_name">현재 비밀번호</p>
          </div>
          <div class="input_box">
            <ValidationProvider name="비밀번호" rules="required">
              <div
                slot-scope="{ errors }"
                style="margin-bottom: 20px; position:relative"
              >
                <div class="value_box">
                  <input type="password" v-model="currentPw" />
                </div>
                <br />
                <span v-if="errors" class="error_box">{{ errors[0] }}</span>
              </div>
            </ValidationProvider>
          </div>
        </div>
        <div class="form_box">
          <div class="label_box">
            <p class="label_name">새 비밀번호</p>
          </div>
          <div class="input_box">
            <ValidationProvider
              name="비밀번호"
              vid="pwd_confirmation"
              rules="required|password|min:8|max:100"
            >
              <div
                slot-scope="{ errors }"
                style="margin-bottom: 20px; position:relative"
              >
                <div class="value_box">
                  <input type="password" v-model="newPw" />
                </div>
                <br />
                <span v-if="errors" class="error_box">{{ errors[0] }}</span>
              </div>
            </ValidationProvider>
          </div>
        </div>
        <div class="form_box">
          <div class="label_box">
            <p class="label_name">새 비밀번호 확인</p>
          </div>
          <div class="input_box">
            <ValidationProvider
              name="비밀번호 확인"
              rules="required|confirmed:pwd_confirmation"
            >
              <div
                slot-scope="{ errors }"
                style="margin-bottom: 20px; height:20px; position:relative"
              >
                <div class="value_box">
                  <input type="password" v-model="checkPw" />
                </div>
                <br />
                <span v-if="errors" class="error_box">{{ errors[0] }}</span>
              </div>
            </ValidationProvider>
          </div>
        </div>
        <div class="form_box">
          <div class="label_box"></div>
          <div class="input_box">
            <button
              class="submit_btn"
              @click="onSubmit()"
              :disabled="invalid || !validated"
            >
              비밀번호 변경
            </button>
          </div>
        </div>
      </ValidationObserver>
    </div>
  </div>
</template>

<script>
import { ValidationProvider, ValidationObserver } from "vee-validate";
import { mapActions, mapState } from "vuex";
export default {
  components: {
    ValidationProvider,
    ValidationObserver
  },
  data() {
    return {
      currentPw: "",
      newPw: "",
      checkPw: "",
      profilePic:
        localStorage.getItem("image") == "null" || ""
          ? require("../../../public/images/user.png")
          : localStorage.getItem("image"),
      name: localStorage.getItem("username")
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
          ? require("../../../public/images/user.png")
          : localStorage.getItem("image");
      this.profilePic = tmp;
    }
  },
  methods: {
    ...mapActions("auth", ["changePassword", "SHA256", "logout"]),
    async onSubmit() {
      let oldHash = "";
      let newHash = "";
      await this.SHA256(String(this.currentPw)).then(res => {
        oldHash = res;
      });
      await this.SHA256(String(this.newPw)).then(res => {
        newHash = res;
      });
      const params = {
        new_password1: newHash,
        new_password2: newHash,
        old_password: oldHash
      };
      await this.changePassword(params);
      alert("다시 로그인해주세요");
      this.logout();
    }
  }
};
</script>

<style scoped>
.right_body_box {
  border-style: none;
  width: 100%;
}
.all_box {
  width: 100%;
  border-style: none;
}
.photo_box {
  display: flex;
  width: 100%;
  margin-top: 30px;
  margin-bottom: 20px;
}
.form_box {
  display: flex;
  width: 100%;
}
.label_box {
  width: 30%;
  text-align: right;
  padding-right: 32px;
  display: flex;
  justify-content: flex-end;
  font-weight: bold;
}
.label_name {
  padding-top: 7px;
}
.input_box {
  width: 70%;
  display: flex;
  justify-content: left;
}
input,
textarea {
  width: 80%;
  height: 100%;
  width: 97%;
}
.value_box {
  border: 1px solid silver;
  width: 25vw;
  height: 40px;
  background: rgb(248, 248, 248);
}
.photo_frame {
  width: 50px;
  height: 50px;
  display: flex;
  justify-content: right;
}
.photo {
  width: 100%;
  height: 100%;
  border-radius: 50%;
}
.user_id {
  text-align: left;
  font-size: 26px;
  padding-top: 5px;
}
.change_photo_btn {
  width: 100%;
  text-align: left;
  font-size: 13px;
  position: relative;
  bottom: 10px;
  color: rgb(0, 140, 255);
  font-weight: bold;
}
.text_box {
  padding: 0;
}
.submit_btn:disabled {
  background: lightblue;
}
.submit_btn {
  background: rgb(96, 187, 218);
  color: white;
  width: 120px;
  height: 30px;
  border-radius: 5%;
  margin-top: 40px;
}
.error_box {
  width: 100%;
  position: absolute;
  color: red;
  background-color: unset;
  right: 50%;
  top: 50px;
  left: 0px;
  font-size: 13px;
}
@media screen and (max-width: 600px) {
  .label_box {
    width: 55%;
    font-size: 14px;
    padding-right: 15px;
  }
  .input_box {
    width: 100%;
  }
  .value_box {
    width: 120%;
  }
}
</style>
