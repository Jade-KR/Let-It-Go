<template>
  <div class="right_body_box">
    <div class="all_box">
      <div class="photo_box">
        <div class="label_box">
          <div class="photo_frame" v-if="loading === false">
            <img :src="profilePic" alt="noImage" class="photo" />
          </div>
          <div class="loading" v-else>
            <i class="fa fa-spinner fa-spin"></i>
          </div>
        </div>
        <div class="input_box">
          <div class="photo_desc">
            <h1 class="user_id">{{ name }}</h1>
            <div class="filebox" v-if="photoCheck === true">
              <label for="ex_file">프로필 사진 변경</label>
              <input type="file" id="ex_file" @change="changeToUrl" />
            </div>

            <div class="filebox" v-else>
              <label for="ex_file2">프로필 사진 변경</label>
              <ProfileModal @loading="loading = true" @stop="loading = false">
                <input type="button" id="ex_file2" slot="click" />
              </ProfileModal>
            </div>
          </div>
        </div>
      </div>
      <ValidationObserver ref="obs" v-slot="{ invalid }">
        <div class="form_box">
          <div class="label_box">
            <p class="label_name">닉네임</p>
          </div>
          <div class="input_box">
            <ValidationProvider name="닉네임" rules="nickname|max:12|required">
              <div
                slot-scope="{ errors }"
                style="margin-bottom: 20px; height:20px; position:relative"
              >
                <div class="value_box">
                  <input type="text" v-model="nickname" />
                </div>
                <br />
                <span v-if="errors" class="error_box">{{ errors[0] }}</span>
              </div>
            </ValidationProvider>
          </div>
        </div>
        <div class="form_box">
          <div class="label_box">
            <p class="label_name">소개</p>
          </div>
          <div class="input_box">
            <div class="value_box_textarea">
              <textarea v-model="comment" rows="3" cols="20" />
            </div>
          </div>
        </div>

        <div class="form_box">
          <div class="label_box">
            <p class="label_name">이메일</p>
          </div>
          <div class="input_box">
            <ValidationProvider name="이메일" rules="email|max:50|required">
              <div
                slot-scope="{ errors }"
                style="margin-bottom: 20px; height:20px; position:relative"
              >
                <div class="value_box">
                  <input type="text" v-model="email" />
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
            <button class="submit_btn" @click="onSubmit()" :disabled="invalid">
              제출
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
import ProfileModal from "./ProfileModal";
export default {
  components: {
    ValidationProvider,
    ValidationObserver,
    ProfileModal
  },
  data() {
    return {
      profilePic:
        localStorage.getItem("image") == "null" || ""
          ? require("../../../public/images/user.png")
          : localStorage.getItem("image"),
      nickname: localStorage.getItem("nickname"),
      comment: localStorage.getItem("comment"),
      email: localStorage.getItem("email"),
      name: localStorage.getItem("username"),
      loading: false,
      photoCheck: localStorage.getItem("image") == "null" || "" ? true : false,
      dialog: false
    };
  },
  methods: {
    ...mapActions("user", ["updateImg", "updateInfo"]),
    async changeToUrl(e) {
      let file = e.target.files[0];
      let reader = new FileReader();
      reader.onload = async a => {
        a;
        this.loading = true;
        await this.updateImg(file);
        this.loading = false;
      };
      if (file) {
        reader.readAsDataURL(file);
      }
    },
    async onSubmit() {
      const params = {
        nickname: this.nickname,
        comment: this.comment,
        email: this.email,
        id: localStorage.getItem("pk")
      };
      const result = await this.updateInfo(params);
      if (result === "이미 존재하는 이메일입니다.") {
        this.email = localStorage.getItem("email");
        alert(result);
        return;
      } else {
        alert("변경이 완료되었습니다.");
      }
      localStorage.setItem("nickname", this.nickname);
      localStorage.setItem("email", this.email);
      localStorage.setItem("comment", this.comment);
    }
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
      this.photoCheck =
        localStorage.getItem("image") == "null" || "" ? true : false;
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
  margin-bottom: 30px;
}
.label_box {
  width: 40%;
  text-align: right;
  padding-right: 32px;
  display: flex;
  justify-content: flex-end;
  font-weight: bold;
  padding-left: 24px;
}
.label_name {
  padding-top: 7px;
}
.input_box {
  width: 100%;
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
.value_box_textarea {
  border: 1px solid silver;
  width: 25vw;
  height: 100px;
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
  font-size: 20px;
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
  width: 60px;
  height: 30px;
  border-radius: 10%;
}
.filebox label {
  display: inline-block;
  padding: 0;
  color: rgb(0, 140, 255);
  font-size: 13px;
  vertical-align: middle;
  cursor: pointer;
  border: none;
  text-align: left;
  font-weight: bold;
}

.filebox input[type="file"] {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  border: 0;
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
.loading {
  width: 50px;
  border-radius: 50%;
  background: rgb(243, 243, 243);
  height: 50px;
  text-align: center;
  line-height: 50px;
}
#ex_file2 {
  display: none;
}
@media screen and (max-width: 600px) {
  .label_box {
    width: 30%;
    padding-left: 0;
  }
  .input_box {
    width: 100%;
  }
  input,
  textarea {
    width: 100%;
  }
  .value_box {
    width: 140%;
  }
  .value_box_textarea {
    width: 91%;
  }
}
</style>
