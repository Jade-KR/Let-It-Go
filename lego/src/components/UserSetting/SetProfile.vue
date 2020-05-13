<template>
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
</template>

<script>
export default {};
</script>

<style scoped>
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