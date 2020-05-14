<template>
  <div class="right_body_box">
    <div class="all_box">
      <div class="photo_box">
        <div class="label_box">
          <div class="photo_frame">
            <img
              src="https://images.unsplash.com/photo-1472457974886-0ebcd59440cc?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=500&q=60"
              alt
              class="photo"
            />
          </div>
        </div>
        <div class="input_box">
          <div class="photo_desc">
            <h1 class="user_id">Jade</h1>
            <button class="change_photo_btn">프로필 사진 바꾸기</button>
          </div>
        </div>
      </div>
      <div class="form_box">
        <div class="label_box">
          <p class="label_name">닉네임</p>
        </div>
        <div class="input_box">
          <v-col cols="12" sm="6" md="10" class="text_box">
            <v-text-field solo dense></v-text-field>
          </v-col>
        </div>
      </div>
      <div class="form_box">
        <div class="label_box">
          <p class="label_name">소개</p>
        </div>
        <div class="input_box">
          <v-col cols="12" md="10" class="text_box">
            <v-textarea solo name="input-7-4" rows="3"></v-textarea>
          </v-col>
        </div>
      </div>
      <div class="form_box">
        <div class="label_box">
          <p class="label_name">이메일</p>
        </div>
        <div class="input_box">
          <v-col cols="12" sm="6" md="10" class="text_box">
            <v-text-field solo dense></v-text-field>
          </v-col>
        </div>
      </div>
      <div class="form_box">
        <div class="label_box"></div>
        <div class="input_box">
          <button class="submit_btn">제출</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {};
</script>

<style scoped>
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
input,
textarea {
  width: 80%;
  height: 100%;
  border: silver 1px solid;
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
.submit_btn {
  background: lightblue;
  color: white;
  width: 50px;
  height: 30px;
  border-radius: 10%;
}
</style>