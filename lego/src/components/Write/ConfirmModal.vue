<template>
  <div>
    <v-dialog v-model="dialog_add_inven" width="400px" class="modal_box">
      <template v-slot:activator="{ on }">
        <div v-on="on">
          <slot name="add_inven" />
        </div>
      </template>

      <v-card class="delete_box">
        <div class="delete_border">
          <h2 class="delete_title">완성 작품인가요? 하위 설계도 인가요?</h2>
          <div class="check_box">
            <button class="delete_btn" @click="onSubmit(1)">완성품</button>
            <button class="cancle_btn" @click="onSubmit(0)">
              하위 설계도
            </button>
          </div>
        </div>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
import { mapActions, mapMutations } from "vuex";

export default {
  data() {
    return {
      dialog_add_inven: false
    };
  },
  methods: {
    ...mapActions("write", ["onWriteSubmit"]),
    ...mapMutations("write", ["setIsProduct"]),
    async onSubmit(value) {
      await this.setIsProduct(value);
      this.onWriteSubmit();
    }
  }
};
</script>

<style scoped>
.delete_box {
  width: 100%;
  height: 210px;
  display: flex;
}
.delete_border {
  border: 3px rgb(255, 214, 139) solid;
  width: 95%;
  height: 90%;
  margin: auto;
}
.delete_title {
  text-align: center;
  width: fit-content;
  margin: auto;
  margin-top: 10px;
  border-bottom: rgb(255, 213, 134) 2px dotted;
}
.delete_body {
  text-align: center;
  font-weight: bold;
  color: black;
  padding-bottom: 0;
}
.delete_btn {
  width: 100px;
  border-radius: 5%;
  font-weight: bold;
  color: green;
  border: 1px solid green;
  transition: ease-in-out 0.3s;
  margin-right: 20px;
  font-size: 20px;
  padding: 3px 6px;
}
.delete_btn:hover {
  background-color: green;
  color: white;
}
.cancle_btn {
  margin: 0px 10px;
  width: 100px;
  border-radius: 5%;
  color: black;
  font-weight: bold;
  border: 1px solid gold;
  font-size: 20px;
  padding: 3px 6px;
}
.cancle_btn:hover {
  background-color: gold;
  color: white;
}
.check_box {
  text-align: center;
  margin-top: 50px;
}
</style>
