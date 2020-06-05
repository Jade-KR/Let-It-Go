<template>
  <div>
    <v-dialog v-model="dialog_add_del" width="400px" class="modal_box">
      <template v-slot:activator="{ on }">
        <div v-on="on">
          <slot name="all_del" />
        </div>
      </template>

      <v-card class="delete_box">
        <div class="delete_border">
          <h2 class="delete_title">모두 삭제 하겠습니까?</h2>
          <v-card-text class="delete_body">
            해당 설계도에 필요한
            <b style="color: gold; font-size: 20px;">모든 부품</b>들을 <br />
            내 부품에서
            <b style="color: red; font-size: 20px;">삭제</b>합니다.
          </v-card-text>
          <v-card-actions>
            <v-spacer></v-spacer>
            <button class="delete_btn" @click="deleteAll()">삭제</button>
            <button class="cancle_btn" @click="dialog_add_del = false">
              취소
            </button>
          </v-card-actions>
        </div>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
export default {
  data() {
    return {
      dialog_add_del: false
    };
  },
  methods: {
    deleteAll() {
      this.$emit("deleteAll");
      this.dialog_add_del = false;
    }
  }
};
</script>

<style scoped>
.delete_box {
  width: 100%;
  height: 180px;
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
  width: 60px;
  border-radius: 5%;
  font-weight: bold;
  color: red;
  border: 1px solid red;
  transition: ease-in-out 0.3s;
}
.cancle_btn {
  margin: 0px 10px;
  width: 60px;
  border-radius: 5%;
  color: black;
  font-weight: bold;
}
</style>
