<template>
  <div class="text-center">
    <v-dialog v-model="dialog" width="440px" class="modal_box">
      <template v-slot:activator="{ on }">
        <div v-on="on">
          <slot name="click" />
        </div>
      </template>

      <v-card class="modify_box">
        <div class="modify_border">
          <h2 class="header">내 부품에 추가</h2>
          <div class="form_box">
            <div class="label_box">
              <p class="label_name">부품 ID</p>
            </div>
            <div class="input_box">
              <v-col cols="12" sm="6" md="10" class="text_box">
                <v-text-field
                  solo
                  dense
                  type="text"
                  :value="this.partId"
                  disabled
                ></v-text-field>
              </v-col>
            </div>
          </div>
          <div class="form_box">
            <div class="label_box">
              <p class="label_name">부품 색</p>
            </div>
            <div class="input_box">
              <div class="color_box" :style="`background: #${this.rgb};`"></div>
            </div>
          </div>
          <div class="form_box">
            <div class="label_box">
              <p class="label_name">추가할 수량</p>
            </div>
            <div class="input_box">
              <v-col cols="12" sm="6" md="5" class="text_box">
                <v-text-field
                  :value="cnt"
                  v-model="cnt"
                  solo
                  dense
                  type="number"
                  step="1"
                  min="0"
                ></v-text-field>
              </v-col>
            </div>
          </div>
          <div class="form_box">
            <div class="label_box"></div>
            <div class="input_box">
              <button class="submit_btn" @click="submit">추가</button>
            </div>
          </div>
        </div>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
import { mapActions } from "vuex";
export default {
  props: {
    partId: { type: String, default: "" },
    colorId: { type: Number, default: 0 },
    quantity: { type: Number, default: 0 },
    rgb: { type: String, default: "" },
    idx: { type: Number, default: 0 }
  },
  data() {
    return {
      dialog: false,
      loading: false,
      cnt: 0
    };
  },
  watch: {
    quantity() {
      this.cnt = this.quantity;
    }
  },
  mounted() {
    this.cnt = this.quantity;
  },
  methods: {
    ...mapActions("Parts", ["updateParts"]),
    async submit() {
      const info = [
        {
          part_id: String(this.partId),
          color_id: Number(this.colorId),
          qte: Number(this.cnt)
        }
      ];
      await this.updateParts({ UpdateList: info });
      this.$emit("update");
      this.dialog = false;
    }
  }
};
</script>

<style scoped>
.modify_box {
  height: 320px;
  display: flex;
}
.modify_border {
  border: 3px rgb(255, 214, 139) solid;
  width: 95%;
  height: 95%;
  margin: auto;
}
.header {
  text-align: center;
  border-bottom: 2px dotted rgb(255, 214, 139);
  width: fit-content;
  margin: auto;
  margin-top: 10px;
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
.text_box {
  padding: 0;
}
.submit_btn {
  background: rgb(106, 190, 218);
  color: white;
  width: 80px;
  height: 30px;
  border-radius: 10px;
  margin-bottom: 10px;
  margin-left: 50px;
}
.color_box {
  width: 70px;
  height: 20px;
  border-radius: 15px;
  margin-top: 9px;
}
</style>
