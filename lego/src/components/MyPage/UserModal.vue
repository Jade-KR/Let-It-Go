<template>
  <div class="text-center">
    <v-dialog v-model="dialog" width="300" class="modal_box">
      <template v-slot:activator="{ on }">
        <div v-on="on">
          <slot name="click" />
        </div>
      </template>

      <v-card class="menu_box">
        <div
          class="menu"
          v-for="(menu, idx) in menus"
          :key="`menu${idx}`"
          @click="goSetting(menu, idx)"
        >
          <p class="menu_name">{{ menu }}</p>
        </div>
        <div class="menu" @click="member()">
          <p class="menu_name">멤버소개</p>
        </div>
        <div class="menu" @click="admin()" v-if="isStaff === 'true'">
          <p class="menu_name">관리자페이지</p>
        </div>
        <div class="menu" @click="logout()">
          <p class="menu_name">로그아웃</p>
        </div>
        <div class="menu" @click="dialog = false">
          <p class="menu_name">취소</p>
        </div>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
import { mapActions } from "vuex";
export default {
  data() {
    return {
      dialog: false,
      menus: ["프로필 편집", "비밀번호 변경", "레고레일"],
      isStaff: localStorage.getItem("isStaff")
    };
  },
  methods: {
    ...mapActions("auth", ["logout"]),
    goSetting(title, idx) {
      this.$router.push({
        name: "UserSetting",
        params: { title: title, idx: idx }
      });
    },
    member() {
      this.$router.push("/member");
    },
    admin() {
      this.$router.push("/admin");
    }
  }
};
</script>

<style scoped>
.menu_box {
  height: 250px;
  display: flex;
  flex-flow: column nowrap;
  border: rgb(255, 140, 46) 4px solid;
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
  border-bottom: gold 1px solid;
}
.menu:hover {
  cursor: pointer;
  background: rgb(0, 112, 0);
}
.menu:hover .menu_name {
  font-weight: bold;
  border-bottom: gold 2px solid;
}
.menu > p {
  margin: 0;
  color: white;
}
hr {
  border: gold 1px solid;
}
</style>
