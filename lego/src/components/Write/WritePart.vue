<template>
  <div>
    <div>
      <div id="part_input">
        <div class="star">
          *
        </div>
        <v-autocomplete
          v-model="partIdx"
          :items="partList"
          filled
          color="rgb(255, 215, 0)"
          background-color="white"
          item-text="name"
          item-value="idx"
          hide-details
          label="부품"
          placeholder="부품을 골라주세요"
        />
      </div>
      <div id="color_input">
        <div class="star">
          *
        </div>
        <v-autocomplete
          v-model="selectedColor"
          :items="partColor"
          filled
          chips
          color="rgb(255, 215, 0)"
          background-color="white"
          item-text="colorName"
          item-value="colorRgb"
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
            @click="partsDelete(part.id, part.color)"
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
      <button @click="onSubmit()" class="after_btn" :disabled="!flag">
        글작성
      </button>
    </div>
  </div>
</template>

<script>
import LegoParts from "../../../jsonData/LegoParts.json";
import LegoColors from "../../../jsonData/LegoColors.json";
import { mapState, mapActions, mapMutations } from "vuex";

export default {
  data() {
    return {
      partList: LegoParts.rows.map((e, i) => {
        return {
          name: e[0] + " " + e[1],
          idx: i,
          img: e[2]
        };
      }),
      partQuantity: 0,
      partIdx: [],
      partColor: LegoColors.rows.map(color => {
        return {
          colorName: color[1],
          colorRgb: color[2]
        };
      }),
      selectedColor: "",
      flag: false
    };
  },
  computed: {
    ...mapState({
      enrolledPart: state => state.write.enrolledPart,
      step: state => state.write.step,
      currentStep: state => state.write.currentStep,
      model: state => state.write.model
    })
  },
  watch: {
    enrolledPart() {
      console.log("aaa", this.enrolledPart);
      if (this.enrolledPart.length !== 0) {
        this.flag = true;
      } else {
        this.flag = false;
      }
    }
  },
  mounted() {
    if (this.enrolledPart.length !== 0) {
      this.flag = true;
    }
  },
  methods: {
    ...mapActions("write", ["prev"]),
    ...mapActions("write", ["enrollPart"]),
    ...mapActions("write", ["deletePart"]),
    ...mapActions("write", ["onWriteSubmit"]),
    ...mapMutations("write", ["setSteps"]),
    ...mapMutations("write", ["setCurrentStep"]),
    goStep(idx) {
      if (this.currentStep >= idx || this.step >= idx) {
        this.setCurrentStep(idx);
      }
    },
    onStep(idx) {
      this.setStep(idx);
    },
    onSubmit() {
      // console.log("submit");
      // console.log(this.model);
      this.onWriteSubmit();
    },
    onPrev(idx) {
      const params = {
        idx: idx,
        step: 3
      };
      this.prev(params);
    },
    partEnroll() {
      if (
        this.partQuantity === 0 ||
        this.partQuantity === "" ||
        this.selectedColor === "" ||
        this.selectedColor === undefined ||
        this.partIdx === undefined ||
        this.partIdx.length === 0
      ) {
        alert("필수값을 채워 주세요");
        return;
      }
      const params = {
        partName: this.partList[this.partIdx]["name"],
        partImg: this.partList[this.partIdx]["img"],
        partColor: this.selectedColor,
        partQuantity: this.partQuantity
      };
      this.enrollPart(params);
      this.partIdx = [];
      this.selectedColor = "";
      this.partQuantity = 0;
    },
    partsDelete(name, color) {
      const params = {
        partName: name,
        partColor: color
      };
      this.deletePart(params);
    }
  }
};
</script>

<style scoped>
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
</style>
