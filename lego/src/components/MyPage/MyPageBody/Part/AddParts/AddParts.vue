<template>
  <div class="text-center">
    <v-dialog v-model="dialog" width="800px" class="modal_box">
      <template v-slot:activator="{ on }">
        <div v-on="on">
          <slot name="click" />
        </div>
      </template>

      <v-card class="menu_box">
        <div class="title_box">
          <div class="search_menus">
            <button
              class="search_by_id"
              @click="currentState = 0"
              :style="currentState === 0 ? menuStyle[0] : menuStyle[1]"
            >
              ID로 찾기
            </button>
            <button
              class="search_by_img"
              @click="checkImg()"
              :style="currentState === 1 ? menuStyle[0] : menuStyle[1]"
            >
              이미지로 찾기
            </button>
          </div>
          <div class="close">
            <i class="fas fa-times" @click="dialog = 0"></i>
          </div>
        </div>
        <div style="padding: 0 20px 20px 20px;">
          <SearchById v-if="currentState === 0" @close="close"></SearchById>
          <SearchByImg v-if="currentState === 1" @close="close"></SearchByImg>
        </div>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
import SearchById from "./SearchById";
import SearchByImg from "./SearchByImg";
import { mapActions } from "vuex";

export default {
  components: {
    SearchById,
    SearchByImg
  },
  data() {
    return {
      dialog: false,
      loading: false,
      currentState: 0,
      menuStyle: [
        { fontWeight: "bold", background: "rgb(255, 212, 93)" },
        { fontWeight: "normal", background: "rgb(235, 213, 155)" }
      ]
    };
  },
  methods: {
    ...mapActions("Parts", ["changeStep"]),
    checkImg() {
      this.currentState = 1;
      this.changeStep("start");
    },
    close() {
      this.$emit("close");
      this.dialog = false;
    }
  }
};
</script>

<style scoped>
.menu_box {
  height: fit-content;
}
.title_box {
  display: flex;
  align-items: baseline;
  border-bottom: silver 1px solid;
  margin-bottom: 20px;
}
.close {
  flex-basis: 3%;
  text-align: right;
  height: 100%;
  font-size: 20px;
  margin-right: 10px;
}
.close > i {
  cursor: pointer;
}
.search_menus {
  display: flex;
  flex-basis: 97%;
  justify-content: space-between;
  height: fit-content;
}
.search_by_id {
  flex-basis: 50%;
  border-right: 1px solid silver;
  font-size: 23px;
  background: rgb(235, 213, 155);
}
.search_by_img {
  flex-basis: 50%;
  border-right: 1px solid silver;
  font-size: 23px;
  background: rgb(235, 213, 155);
}
</style>
