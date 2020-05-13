<template>
  <div class="right_body_box">
    <div class="all_box">
      <div class="form_box">
        <div class="label_box">현재 비밀번호</div>
        <div class="input_box">
          <input type="text" />
        </div>
      </div>
      <div class="form_box">
        <div class="label_box">새 비밀번호</div>
        <div class="input_box">
          <input type="text" />
        </div>
      </div>
      <div class="form_box">
        <div class="label_box">비밀번호 확인</div>
        <div class="input_box">
          <input type="text" />
        </div>
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