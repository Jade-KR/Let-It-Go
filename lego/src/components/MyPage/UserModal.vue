<template>
  <div class="text-center">
    <v-dialog v-model="dialog" width="300" class="modal_box">
      <template v-slot:activator="{ on }">
        <div v-on="on">
          <slot name="click" />
        </div>
      </template>

      <v-card class="menu_box">
        <div class="menu" v-for="(menu, idx) in menus" :key="`menu${idx}`" @click="goSetting(idx)">
          <p>{{menu}}</p>
        </div>
        <div class="menu">
          <p>로그아웃</p>
        </div>
        <div class="menu" @click="dialog=false">
          <p>취소</p>
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
      menus: ["프로필 편집", "비밀번호 변경", "분류기 설정"]
    };
  },
  methods: {
    goSetting(idx) {
      this.$router.push({ name: "UserSetting", params: { idx: idx } });
    }
  }
};
</script>

<style scoped>
.menu_box {
  height: 250px;
  display: flex;
  flex-flow: column nowrap;
  border: rgb(255, 115, 0) 4px solid;
}
.menu {
  width: 100%;
  text-align: center;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  background: green;
  transition: ease-in;
  transition-duration: 0.2s;
}
.menu:hover {
  cursor: pointer;
  background: rgb(0, 82, 0);
}
.menu > p {
  margin: 0;
  color: white;
}
hr {
  border: gold 1px solid;
}
</style>