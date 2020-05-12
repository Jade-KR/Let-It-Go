<template>
  <div>
    <div class="container">
      <div class="header">
        <MypageHeader></MypageHeader>
      </div>
      <hr />
      <div class="body_menu_bar">
        <button class="menu" v-for="i in menus.length" :key="i">
          <i :class="menuIcons[i-1]"></i>
          {{menus[i-1]}}
        </button>
      </div>
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
    return {
      menus: ["설계도", "부품", "좋아요", "기타", "등등"],
      menuIcons: [
        "fas fa-scroll",
        "fas fa-cubes",
        "fas fa-heart",
        "fas fa-heart",
        "fas fa-heart"
      ]
    };
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
  border: rgb(252, 193, 85) solid 1.2px;
}
.body_menu_bar {
  display: flex;
  border-style: none;
  height: 50px;
  margin-bottom: 20px;
  margin-top: 10px;
  justify-content: center;
}
.menu {
  font-size: 17px;
  color: rgb(160, 159, 159);
  margin-right: 40px;
  width: 6vw;
}
.menu:hover {
  color: black;
  font-size: 18px;
  font: x-large;
}
.body {
  border-style: none;
  height: 100%;
  width: 100%;
}
</style>
