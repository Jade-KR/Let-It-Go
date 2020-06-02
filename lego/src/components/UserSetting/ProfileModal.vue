<template>
  <div>
    <v-dialog v-model="dialog" width="300px" class="modal_box">
      <template v-slot:activator="{ on }">
        <div v-on="on">
          <slot name="click" />
        </div>
      </template>
      <v-card class="profile_modal_container">
        <h2 class="profile_modal_header">프로필 사진 변경</h2>
        <div class="profile_modal_menus">
          <label for="modal_ex_file">사진 변경</label>
          <input type="file" id="modal_ex_file" @change="changeToUrl" />
        </div>
        <div class="profile_modal_menus2">
          <label for="modal_ex_file2">현재 사진 삭제</label>
          <input type="button" id="modal_ex_file2" @click="cleanImg()" />
        </div>
        <div class="profile_modal_menus3" @click="dialog=false">취소</div>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
import { mapActions } from "vuex";
export default {
  data() {
    return {
      dialog: false
    };
  },
  methods: {
    ...mapActions("user", ["updateImg", "updateInfo", "deleteImg"]),
    async changeToUrl(e) {
      const that = this;
      let file = e.target.files[0];
      let reader = new FileReader();
      reader.onload = async a => {
        that.dialog = false;
        this.$emit("loading");
        await this.updateImg(a.target.result);
        this.$emit("stop");
      };
      if (file) {
        reader.readAsDataURL(file);
      }
    },
    async cleanImg() {
      const params = { profile_url: "null" };
      this.dialog = false;
      await this.deleteImg(params);
    }
  }
};
</script>

<style scoepd>
.profile_modal_container {
  width: 100%;
  height: fit-content;
  background: white;
  padding-bottom: 20px;
}
.profile_modal_header {
  text-align: center;
  margin-bottom: 20px;
  border-bottom: orange dotted 2px;
  width: fit-content;
  margin: auto;
  margin-bottom: 20px;
}
.profile_modal_menus {
  width: 100%;
  height: 30px;
  position: relative;
  margin-bottom: 10px;
}
.profile_modal_menus2 {
  width: 100%;
  height: 30px;
  position: relative;
  margin-bottom: 10px;
}
.profile_modal_menus3 {
  width: 100%;
  height: 100%;
  display: inline-block;
  font-size: 15px;
  vertical-align: middle;
  cursor: pointer;
  border: none;
  font-weight: bold;
  text-align: center;
  margin-top: 10px;
}
.profile_modal_menus label {
  width: 100%;
  height: 100%;
  display: inline-block;
  color: rgb(0, 140, 255);
  font-size: 15px;
  vertical-align: middle;
  cursor: pointer;
  border: none;
  font-weight: bold;
  text-align: center;
  line-height: 30px;
}

.profile_modal_menus input[type="file"] {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  border: 0;
}
.profile_modal_menus2 label {
  width: 100%;
  height: 100%;
  display: inline-block;
  color: red;
  font-size: 15px;
  vertical-align: middle;
  cursor: pointer;
  border: none;
  text-align: left;
  font-weight: bold;
  text-align: center;
  line-height: 30px;
}

.profile_modal_menus2 input[type="file"] {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  border: 0;
}
</style>