<template>
  <div>
    <div class="bg">
      <div class="whole_box">
        <div class="left_menu_box">
          <div class="menu_box" v-for="(menu, idx) in menus" :key="menu">
            <p :id="`menu${idx}`" @click="menuState(idx, menus.length)">{{menu}}</p>
          </div>
        </div>
        <div class="right_body_box">
          <div class="all_box">
            <div class="form_box">
              <div class="label_box">사진</div>
              <div class="input_box">
                <input type="text" />
              </div>
            </div>
            <div class="form_box">
              <div class="label_box">닉네임</div>
              <div class="input_box">
                <input type="text" />
              </div>
            </div>
            <div class="form_box">
              <div class="label_box">소개</div>
              <div class="input_box">
                <textarea name id cols="30" rows="3"></textarea>
              </div>
            </div>
            <div class="form_box">
              <div class="label_box">이메일</div>
              <div class="input_box">
                <input type="text" value="ijung1@naver.com" />
              </div>
            </div>
            <div class="form_box">
              <div class="label_box"></div>
              <div class="input_box"></div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: { idx: Number },
  data() {
    return {
      menus: ["프로필 편집", "비밀번호 변경", "분류기 설정"],
      currentState: 0
    };
  },
  mounted() {
    const i = this.idx;
    const n = this.menus.length;
    this.menuState(i, n);
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
.bg {
  text-align: center;
  height: 1000px;
  width: 100%;
  display: flex;
  justify-content: center;
  background: white;
}
.whole_box {
  border: 1px silver solid;
  width: 55%;
  height: fit-content;
  display: flex;
  padding: 0;
  position: absolute;
  margin-top: 50px;
}
.left_menu_box {
  border: 1px silver solid;
  width: 25%;
  height: 500px;
}
.right_body_box {
  border: 1px silver solid;
  width: 75%;
  height: fit-content;
}
.menu_box {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 60px;
}
.menu_box:hover {
  background: #e6e6e6;
}
.menu_box > p {
  margin: 0;
  width: 80%;
  height: 100%;
  padding-top: 20px;
  text-align: left;
}
.menu_box:hover {
  cursor: pointer;
}
.all_box {
  width: 100%;
}
.form_box {
  display: flex;
  width: 100%;
}
.label_box {
  border: silver 1px solid;
  width: 20%;
  text-align: right;
  padding-right: 20px;
}
.input_box {
  border: silver 1px solid;
  width: 80%;
}
input,
textarea {
  width: 100%;
  background: rgb(240, 240, 240);
  height: 100%;
}
</style>