<template>
  <div class="text-center">
    <v-dialog v-model="dialog" width="400px" class="modal_box">
      <template v-slot:activator="{ on }">
        <div v-on="on">
          <slot name="click" />
        </div>
      </template>

      <v-card class="menu_box">
        <div class="title_box">
          <h3 class="title">부품을 등록하세요!</h3>
          <div class="close" @click="dialog = 0">
            <i class="fas fa-times"></i>
          </div>
        </div>
        <div class="form_box">
          <div class="label_box">
            <p class="label_name">부품 ID</p>
          </div>
          <div class="input_box">
            <v-col cols="12" sm="6" md="10" class="text_box">
              <v-text-field solo dense type="text" v-model="partId"></v-text-field>
            </v-col>
          </div>
        </div>
        <div class="form_box">
          <div class="label_box">
            <p class="label_name">컬러</p>
          </div>
          <div class="input_box">
            <v-col cols="12" sm="6" md="10" class="text_box">
              <v-text-field solo dense type="text" v-model="partColor"></v-text-field>
            </v-col>
          </div>
        </div>
        <div class="form_box">
          <div class="label_box">
            <p class="label_name">수량</p>
          </div>
          <div class="input_box">
            <v-col cols="12" sm="6" md="10" class="text_box">
              <v-text-field solo dense type="number" v-model="partCnt"></v-text-field>
            </v-col>
          </div>
        </div>
        <div class="form_box">
          <div class="label_box">
            <p class="label_name"></p>
          </div>
          <div class="input_box">
            <button class="submit_btn">
              <i class="fas fa-plus"></i>&nbsp;부품 추가
            </button>
          </div>
        </div>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
export default {
  data() {
    return {
      dialog: false,
      partId: "",
      partColor: "",
      partCnt: 0
    };
  },
  methods: {}
};
</script>

<style scoped>
.menu_box {
  height: max-content;
  border-top: rgb(94, 116, 122) 5px solid;
}
.right_body_box {
  border-style: none;
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
.photo_frame {
  width: 50px;
  height: 50px;
  display: flex;
  justify-content: right;
}
.photo {
  width: 100%;
  height: 100%;
  border-radius: 180%;
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
.submit_btn {
  background: lightblue;
  color: white;
  width: 120px;
  height: 30px;
  border-radius: 5%;
  margin-bottom: 10px;
}
.title_box {
  display: flex;
  align-items: baseline;
  border-bottom: silver 1px solid;
  margin-bottom: 20px;
}
.title {
  flex-basis: 90%;
  margin: 0;
  margin-left: 10px;
  font-size: 20px;
  padding: 10px 0;
}
.close {
  flex-basis: 10%;
  text-align: center;
  cursor: pointer;
  height: 100%;
  padding: 10px;
}
</style>