<template>
  <div>
    <v-dialog v-model="dialog" width="800px" class="modal_box">
      <template v-slot:activator="{ on }">
        <div v-on="on">
          <slot name="click" />
        </div>
      </template>
      <div class="modal_box">
        <div class="modal_border">
          <div class="modal_container">
            <h2 class="modal_header">부품 정보 수정</h2>
            <div id="part_input">
              <div class="star">*</div>
              <v-autocomplete
                v-model="partIdx"
                filled
                color="rgb(255, 215, 0)"
                background-color="white"
                item-text="name"
                item-value="idx"
                hide-details
                label="부품"
                :placeholder="String(partId)"
                disabled
              />
            </div>
            <div class="color_cnt_box">
              <div id="color_input">
                <div class="star">*</div>
                <v-autocomplete
                  v-model="selectedColor"
                  :items="partColor"
                  filled
                  chips
                  color="rgb(255, 215, 0)"
                  background-color="white"
                  item-text="colorName"
                  item-value="idx"
                  hide-details
                  label="색상"
                  placeholder="색상을 골라주세요"
                >
                  <template v-slot:selection="data">
                    <v-chip
                      v-bind="data.attrs"
                      :input-value="data.selected"
                      @click="data.select"
                      color="white"
                      style="height: 54px;"
                    >
                      <v-avatar left>
                        <div
                          :style="
                            `background-color: #${data.item.colorRgb}; width: 100%; height: 100%;`
                          "
                        ></div>
                      </v-avatar>
                      {{ data.item.colorName }}
                    </v-chip>
                  </template>
                  <template v-slot:item="data">
                    <template v-if="typeof data.item !== 'object'">
                      <v-list-item-content
                        v-text="data.item"
                      ></v-list-item-content>
                    </template>
                    <template v-else>
                      <v-list-item-avatar>
                        <div
                          :style="
                            `background-color: #${data.item.colorRgb}; width: 100%; height: 100%;`
                          "
                        ></div>
                      </v-list-item-avatar>
                      <v-list-item-content>
                        <v-list-item-title
                          v-html="data.item.colorName"
                        ></v-list-item-title>
                      </v-list-item-content>
                    </template>
                  </template>
                </v-autocomplete>
              </div>
              <div id="quan_input">
                <div class="star star2">*</div>
                <v-text-field
                  label="수량"
                  type="number"
                  min="0"
                  step="1"
                  v-model="partQuantity"
                  hide-details
                  height="55px"
                  color="rgb(255, 215, 0)"
                  style="width: 100px; font-size: 24px;"
                ></v-text-field>
              </div>
            </div>
            <input
              type="submit"
              value="수정 완료"
              id="enroll_btn"
              @click="changeInfo()"
            />
          </div>
        </div>
      </div>
    </v-dialog>
  </div>
</template>

<script>
import LegoColors from "../../../../jsonData/LegoColors.json";
import { mapActions, mapState } from "vuex";

export default {
  props: {
    partId: String,
    colorId: Number,
    quantity: Number,
    idx: Number
  },
  data() {
    return {
      partQuantity: 0,
      partIdx: "",
      partColor: LegoColors.rows.map((color, i) => {
        return {
          colorName: color[1],
          colorRgb: color[2],
          colorId: color[0],
          idx: i
        };
      }),
      selectedColor: "",
      index: "",
      dialog: false
    };
  },
  created() {
    this.index = this.idx;
  },
  mounted() {
    this.selectedColor = this.colorId;
    this.partQuantity = this.quantity;
  },
  computed: {
    ...mapState({
      basket: state => state.Parts.basket,
      pickedPart: state => state.Parts.pickedPart
    }),
    flag: function() {
      return this.basket.length > 0 ? true : false;
    }
  },
  methods: {
    ...mapActions("Parts", [
      "addBasket",
      "deleteBasket",
      "changeStep",
      "updateParts",
      "getUserParts"
    ]),
    changeInfo() {
      if (this.selectedColor === "" || this.partQuantity <= 0) {
        return alert("필수 정보를 입력해주세요.");
      }
      const info = {
        idx: this.index,
        colorId: Number(this.selectedColor),
        quantity: Number(this.partQuantity),
        partId: this.partId
      };
      this.$emit("changedInfo", info);
      this.dialog = false;
    }
  }
};
</script>

<style scoped>
.modal_box {
  width: 100%;
  height: 330px;
  background: white;
}
.modal_border {
  border: rgb(255, 198, 93) 2px solid;
  width: 95%;
  height: 90%;
  margin: auto;
  transform: translateY(15px);
}
.modal_container {
  display: flex;
  flex-flow: column wrap;
  align-items: center;
}
.modal_header {
  border-bottom: 2px dotted rgb(252, 210, 132);
  margin-top: 10px;
}
.color_cnt_box {
  display: flex;
  flex-flow: row nowrap;
  width: 90%;
  align-items: baseline;
}
#part_input {
  width: 90%;
}
#part_input,
#color_input {
  margin-bottom: 20px;
}
#color_input,
#quan_input,
#enroll_btn {
  display: inline-block;
}
#color_input {
  width: 80%;
}
#quan_input {
  margin: 0 20px;
  width: 20%;
}
#enroll_btn {
  padding: 10px;
  background-color: gold;
  width: 20%;
  margin-bottom: 20px;
}
.enroll_img {
  width: 100px;
  height: 100px;
}
.enrolled_parts {
  display: inline-block;
  margin: 0 5px 10px 5px;
  position: relative;
}
.enrolled_parts_box {
  display: flex;
  flex-flow: row wrap;
  justify-content: flex-start;
  margin: auto;
  width: 95%;
}
.enrolled_desc {
  text-align: center;
  display: flex;
  width: 100px;
}
.enrolled_text {
  min-width: 50%;
  display: inline-block;
}
.enrolled_name {
  white-space: nowrap;
  overflow: hidden;
}
.enrolled_quan {
  margin-left: 5px;
  min-width: 50%;
  display: inline-block;
}
.star {
  position: absolute;
  transform: translateX(5px);
  color: red;
  z-index: 1;
}
.star2 {
  transform: translate(-8px, 5px);
}
.delete_btn {
  width: 20px;
  height: 20px;
  position: absolute;
  top: 0;
  transform: translateX(-50px);
  cursor: pointer;
}
.delete_btn:hover {
  background-color: rgba(255, 0, 0, 0.8);
  border-radius: 50%;
}

.before_btn,
.after_btn {
  background-color: gold;
  padding: 10px;
  border-radius: 20px;
  width: 100px;
  margin-top: 20px;
}
.before_btn:hover,
.after_btn:hover {
  background-color: green;
  color: white;
}
.before_btn {
  margin-left: 10px;
  margin-bottom: 10px;
}
.after_btn {
  margin-right: 10px;
  margin-bottom: 10px;
}
.after_btn:disabled {
  background-color: gray;
  color: black;
}
.after_btn:disabled:hover {
  background-color: gray;
  color: black;
}
.basket_list {
  display: flex;
  justify-content: flex-start;
}
.modal_footer {
  display: flex;
  justify-content: space-between;
}
.modal_container {
  background: white;
}
@media screen and (max-width: 600px) {
  #enroll_btn {
    width: 40%;
  }
}
</style>
