<template>
  <div>
    <div class="container">
      <div class="header">
        <MypageHeader></MypageHeader>
      </div>
      <hr />
      <div class="body_menu_bar"></div>
      <div class="body">
        <MypageBody></MypageBody>
      </div>
    </div>
  </div>
</template>

<script>
import MypageHeader from "@/components/MypageHeader.vue";
import MypageBody from "@/components/MypageBody.vue";
export default {
  components: {
    MypageHeader,
    MypageBody
  },
  data() {
    return {};
  }
};
</script>

<style scoped>
/* 큰 레이아웃 */
.container {
  border-style: none;
  align-items: center;
  width: 60%;
  height: 100%;
  margin: auto;
}
.header {
  border-style: none;
  width: 100%;
  height: 200px;
  margin-bottom: 20px;
}
hr {
  border: rgb(252, 193, 85) solid 2px;
}
.body_menu_bar {
  border: black solid 1px;
  height: 50px;
  margin-bottom: 20px;
}
.body {
  border: black solid 1px;
  height: 100%;
  width: 100%;
}
</style>
