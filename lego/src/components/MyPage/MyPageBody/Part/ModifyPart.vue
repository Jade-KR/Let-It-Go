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
          <h2 class="header">수량 변경 & 삭제</h2>
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
              <p class="label_name">변경할 수량</p>
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
              <button class="submit_btn" @click="submit">수정</button>
              <button class="delete_btn" @click="deleteItem">삭제</button>
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
    partId: String,
    colorId: Number,
    quantity: Number,
    rgb: String,
    page: Number,
    idx: Number
  },
  data() {
    return {
      dialog: false,
      loading: false,
      originalCnt: 0,
      cnt: 0
    };
  },
  mounted() {
    this.originalCnt = this.quantity;
    this.cnt = this.quantity;
  },
  methods: {
    ...mapActions("Parts", ["updateParts", "getParts"]),
    async submit() {
      let num = 0;
      if (this.cnt <= 0) {
        num = -Number(this.originalCnt);
      } else if (this.cnt > this.originalCnt) {
        num = Number(this.cnt - this.originalCnt);
      } else {
        num = -Number(this.originalCnt - this.cnt);
      }
      const info = [
        {
          part_id: String(this.partId),
          color_id: Number(this.colorId),
          qte: Number(num)
        }
      ];
      await this.updateParts({ UpdateList: info });
      const params = {
        idx: Number(this.idx),
        quantity: Number(this.cnt)
      };
      this.$emit("update", params);
      this.dialog = false;
    },
    async deleteItem() {
      const info = [
        {
          part_id: String(this.partId),
          color_id: Number(this.colorId),
          qte: Number(-this.originalCnt)
        }
      ];
      await this.updateParts({ UpdateList: info });
      const params = {
        idx: this.idx,
        quantity: Number(0),
        part_id: String(this.partId),
        color_id: Number(this.colorId)
      };
      this.$emit("update", params);
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
}
.delete_btn {
  background: red;
  color: white;
  width: 80px;
  height: 30px;
  margin-left: 30px;
  border-radius: 10px;
}
.color_box {
  width: 70px;
  height: 20px;
  border-radius: 15px;
  margin-top: 9px;
}
</style>
