<template>
  <div>
    <div>
      <div id="part_header">
        <div
          id="part_input_btn"
          @click="setInput('part')"
          :style="inputFlag == 'part' ? btnStyle[0] : btnStyle[1]"
        >
          <i class="fas fa-font"></i>&nbsp; 부품명
        </div>
        <div
          id="img_input_btn"
          @click="setInput('img')"
          :style="inputFlag == 'img' ? btnStyle[0] : btnStyle[1]"
        >
          <i class="fas fa-camera"></i>&nbsp; 이미지
        </div>
      </div>
      <hr
        style="border: 1px solid gold; margin: auto; margin-bottom: 10px; width: 80%;"
      />
      <div id="part_input" v-if="inputFlag === 'part'">
        <div class="star">
          *
        </div>
        <v-autocomplete
          v-model="partIdx"
          :items="partList"
          filled
          color="rgb(255, 215, 0)"
          background-color="white"
          item-text="partName"
          item-value="partIdx"
          hide-details
          label="부품"
          placeholder="하위 설계도 외에 필요한 부품을 골라주세요"
          multiple
        />
      </div>
      <div id="img_input" v-else>
        <pick-category v-if="pickStep === 0"></pick-category>
        <pick-part v-if="pickStep === 1"></pick-part>
      </div>

      <div id="color_input">
        <div class="star">
          *
        </div>
        <v-autocomplete
          v-model="colorIdx"
          :items="partColor"
          filled
          chips
          color="rgb(255, 215, 0)"
          background-color="white"
          item-text="colorName"
          item-value="colorIdx"
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
              <v-list-item-content v-text="data.item"></v-list-item-content>
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
        <div class="star star2">
          *
        </div>
        <v-text-field
          label="수량"
          type="number"
          min="1"
          step="1"
          v-model="partQuantity"
          hide-details
          height="55px"
          color="rgb(255, 215, 0)"
          style="width: 100px; font-size: 24px;"
        ></v-text-field>
      </div>
      <input type="submit" @click="partEnroll()" value="등록" id="enroll_btn" />
    </div>

    <hr
      style="border: 1px solid gold; margin-bottom: 20px;"
      v-if="enrolledPart.length"
    />

    <div class="enrolled_parts">
      <div
        v-for="(part, i) in enrolledPart"
        :key="`part-${i}`"
        class="enrolled_parts"
      >
        <div>
          <img
            src="../../assets/icons/delete.png"
            alt="delete"
            class="delete_btn"
            @click="partsDelete(part.id, part.name, part.color)"
          />
        </div>
        <img
          :src="part.img"
          alt="enroll_img"
          class="enroll_img"
          v-if="part.img"
        />
        <img
          src="../../assets/icons/no_img.jpg"
          alt="enroll_img"
          class="enroll_img"
          v-else
        />
        <div class="enrolled_desc">
          <div class="enrolled_text">
            <div class="enrolled_name">
              {{ part["id"] }}
            </div>
            <div
              class="enrolled_color"
              :style="
                `width: 100%; height: 10px; background-color: #${part.color};`
              "
            ></div>
          </div>
          <div class="enrolled_quan">* {{ part["quantity"] }}</div>
        </div>
      </div>
    </div>

    <div>
      <button @click="onPrev(step - 1)" class="before_btn">
        이전
      </button>
      <div id="enroll_cnt">
        <b style="color: green; font-size: 28px;">{{ enrolledPart.length }}</b
        >종류, 총 <b style="color: green; font-size: 28px;">{{ partQnt }}</b
        >개의 부품이 등록되었습니다.
      </div>
      <button class="after_btn">
        <confirm-modal>
          <div slot="add_inven" :disabled="!flag">
            글작성
          </div>
        </confirm-modal>
      </button>
    </div>
  </div>
</template>

<script>
import { mapState, mapActions, mapMutations } from "vuex";
import PickCategory from "./EnrollByImg/PickCategory.vue";
import PickPart from "./EnrollByImg/PickPart.vue";
import ConfirmModal from "./ConfirmModal.vue";

export default {
  components: {
    PickCategory,
    PickPart,
    ConfirmModal
  },
  data() {
    return {
      btnStyle: [
        {
          fontSize: "24px",
          color: "black"
        },
        {
          fontSize: "18px"
        }
      ],
      inputFlag: "part",
      partQuantity: 0,
      partIdx: [],
      colorIdx: 0,
      flag: false,
      partQnt: 0
    };
  },
  computed: {
    ...mapState({
      enrolledPart: state => state.write.enrolledPart,
      step: state => state.write.step,
      currentStep: state => state.write.currentStep,
      model: state => state.write.model,
      partList: state => state.write.partList,
      partColor: state => state.write.partColor,
      pickStep: state => state.write.pickStep,
      pickedPartByImg: state => state.write.pickedPartByImg
    })
  },
  watch: {
    enrolledPart() {
      this.partQnt = 0;
      if (this.enrolledPart.length !== 0) {
        this.flag = true;
      } else {
        this.flag = false;
      }
      for (let i = 0; i < this.enrolledPart.length; ++i) {
        this.partQnt += Number(this.enrolledPart[i]["quantity"]);
      }
    }
  },
  mounted() {
    if (this.enrolledPart.length !== 0) {
      this.flag = true;
    }
  },
  methods: {
    ...mapActions("write", [
      "prev",
      "enrollPart",
      "deletePart",
      "onWriteSubmit"
    ]),
    ...mapMutations("write", [
      "setSteps",
      "setCurrentStep",
      "setPickStep",
      "setPickedPartByImg",
      "resetPickedPartByImg"
    ]),
    goStep(idx) {
      if (this.currentStep >= idx || this.step >= idx) {
        this.setCurrentStep(idx);
      }
    },
    onStep(idx) {
      this.setStep(idx);
    },
    onPrev(idx) {
      const params = {
        idx: idx,
        step: 3
      };
      this.prev(params);
    },
    setInput(value) {
      if (value === "part") {
        this.inputFlag = "part";
      } else {
        this.inputFlag = "img";
      }
      this.setPickStep(0);
      this.resetPickedPartByImg();
    },
    partEnroll() {
      if (this.pickedPartByImg.length !== 0) {
        if (
          this.partQuantity === 0 ||
          this.partQuantity === "" ||
          this.colorIdx === "" ||
          this.colorIdx === undefined
        ) {
          alert("필수값을 채워 주세요");
          return;
        }
        for (let i = 0; i < this.pickedPartByImg.length; ++i) {
          const params = {
            partName: this.pickedPartByImg[i][0],
            partImg: this.pickedPartByImg[i][1],
            partId: this.pickedPartByImg[i][2],
            partColor: this.partColor[this.colorIdx]["colorRgb"],
            partColorId: this.partColor[this.colorIdx]["colorId"],
            partQuantity: this.partQuantity
          };
          this.enrollPart(params);
        }
        this.resetPickedPartByImg();
        this.colorIdx = "";
        this.partQuantity = 0;
      } else {
        if (
          this.partQuantity === 0 ||
          this.partQuantity === "" ||
          this.colorIdx === "" ||
          this.colorIdx === undefined ||
          this.partIdx === undefined ||
          this.partIdx.length === 0
        ) {
          alert("필수값을 채워 주세요");
          return;
        }
        for (let i = 0; i < this.partIdx.length; ++i) {
          const params = {
            partName: this.partList[this.partIdx[i]]["partName"],
            partImg: this.partList[this.partIdx[i]]["partImg"],
            partId: this.partList[this.partIdx[i]]["partId"],
            partColor: this.partColor[this.colorIdx]["colorRgb"],
            partColorId: this.partColor[this.colorIdx]["colorId"],
            partQuantity: this.partQuantity
          };
          this.enrollPart(params);
        }
        this.partIdx = [];
        this.colorIdx = "";
        this.partQuantity = 0;
      }
    },
    partsDelete(partId, partName, color) {
      const params = {
        partId: partId,
        partName: partName,
        partColor: color
      };
      this.deletePart(params);
    }
  }
};
</script>

<style scoped>
#part_header {
  text-align: center;
  margin-bottom: 20px;
}
#part_input_btn,
#img_input_btn {
  display: inline-block;
  cursor: pointer;
  font-size: 18px;
  padding: 5px;
  margin: 0 120px;
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
  width: 60%;
}
#quan_input {
  margin: 0 20px;
}
#enroll_btn {
  padding: 10px;
  background-color: gold;
  width: 20%;
}
.enroll_img {
  width: 100px;
  height: 100px;
}
.enrolled_parts {
  display: inline-block;
  margin: 0 5px 10px 5px;
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
.after_btn {
  float: right;
}
.after_btn:disabled {
  background-color: gray;
  color: black;
}
.after_btn:disabled:hover {
  background-color: gray;
  color: black;
}
#enroll_cnt {
  text-align: center;
  margin-left: 130px;
  font-size: 20px;
  display: inline-block;
}
</style>
