<template>
  <div class="text-center">
    <v-dialog v-model="dialog" width="400px" class="modal_box">
      <template v-slot:activator="{ on }">
        <div v-on="on">
          <slot name="click" />
        </div>
      </template>

      <v-card>
        <h2 class="header">수량 변경&제거</h2>
        <div class="form_box">
          <div class="label_box">
            <p class="label_name">부품 ID</p>
          </div>
          <div class="input_box">
            <v-col cols="12" sm="6" md="10" class="text_box">
              <v-text-field solo dense type="text" :value="this.partId" disabled></v-text-field>
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
                v-model="quantity"
                solo
                dense
                type="number"
                step="1"
                :value="quantity"
                min="0"
              ></v-text-field>
            </v-col>
          </div>
        </div>
        <div class="form_box">
          <div class="label_box"></div>
          <div class="input_box">
            <button class="delete_btn" @click="deleteItem">삭제</button>
            <button class="submit_btn" @click="submit">수정</button>
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
    page: Number
  },
  mounted() {
    this.originalCnt = this.quantity;
    this.check = this.quantity;
  },
  data() {
    return {
      dialog: false,
      loading: false,
      originalCnt: 0,
      check: 0
    };
  },
  watch: {
    quantity() {
      this.originalCnt = this.quantity;
    }
  },
  methods: {
    ...mapActions("Parts", ["updateParts", "getUserParts"]),
    async submit() {
      let num = 0;
      if (this.quantity <= 0) {
        num = -Number(this.check);
      } else if (this.quantity > this.check) {
        num = Number(this.quantity - this.check);
      } else {
        num = -Number(this.check - this.quantity);
      }
      const params = [
        {
          part_id: String(this.partId),
          color_id: Number(this.colorId),
          qte: Number(num)
        }
      ];
      await this.updateParts({ UpdateList: params });
      await this.getUserParts(this.page);
      this.dialog = false;
      this.originalCnt = this.quantity;
      this.check = this.quantity;
    },
    async deleteItem() {
      const params = [
        {
          part_id: String(this.partId),
          color_id: Number(this.colorId),
          qte: Number(-this.originalCnt)
        }
      ];
      await this.updateParts({ UpdateList: params });
      try {
        await this.getUserParts(this.page);
      } catch {
        await this.getUserParts(this.page - 1);
        this.$emit("pageDown");
      }
      this.dialog = false;
      this.originalCnt = this.quantity;
    }
  }
};
</script>

<style scoped>
.header {
  text-align: center;
  margin-bottom: 20px;
  border-bottom: 1px solid silver;
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
  border-radius: 15%;
  margin-left: 30px;
  margin-bottom: 10px;
}
.delete_btn {
  background: red;
  color: white;
  width: 80px;
  height: 30px;
  border-radius: 15%;
}
.color_box {
  width: 30px;
  height: 20px;
  border-radius: 20%;
  margin-top: 9px;
}
</style>