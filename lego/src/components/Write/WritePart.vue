<template>
  <div>
    <div @click="test()">
      asdf
    </div>
    <div>
      <v-autocomplete
        v-model="partIdx"
        :items="partList"
        filled
        chips
        label="Select"
        item-text="name"
        item-value="idx"
      />
      <input type="number" step="1" min="0" v-model="partCnt" />
      <input type="submit" @click="check()" value="등록" />
    </div>

    <div v-for="(part, i) in enrolledPart" :key="`part-${i}`">
      <img :src="part[1]" alt="enroll_img" class="enroll_img" />
      <div>
        {{ part[0] }}
      </div>
      <div>{{ part[2] }}개</div>
    </div>

    <div>
      <button @click="onPrev(step - 1)" class="before_btn">
        이전
      </button>
      <button @click="onSubmit()" class="after_btn">
        글작성
      </button>
    </div>
  </div>
</template>

<script>
import LegoParts from "../../../jsonData/LegoParts.json";
import { mapState, mapActions, mapMutations } from "vuex";

export default {
  data() {
    return {
      partsListData: LegoParts["rows"],
      partsHeader: LegoParts["header"],
      partList: [],
      partCnt: 0,
      partIdx: ""
    };
  },
  computed: {
    ...mapState({
      enrolledPart: state => state.write.enrolledPart,
      step: state => state.write.step,
      currentStep: state => state.write.currentStep
    })
  },
  mounted() {
    this.onAutoPartList();
  },
  methods: {
    check() {
      const params = {
        partName: this.partList[this.partIdx]["name"],
        partImg: this.partList[this.partIdx]["img"],
        partCnt: this.partCnt
      };
      this.enrollPart(params);
      this.partIdx = [];
      this.partCnt = 0;
    },
    ...mapActions("write", ["prev"]),
    ...mapActions("write", ["enrollPart"]),
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
      this.partIdx = [];
      this.partCnt = 0;
      console.log("submit");
    },
    onPrev(idx) {
      const params = {
        idx: idx,
        step: 3
      };
      this.prev(params);
    },
    onAutoPartList() {
      this.partsListData.forEach((e, i) => {
        this.partList.push({
          name: e[0] + " " + e[1],
          idx: i,
          img: e[2]
        });
      });
    }
  }
};
</script>

<style scoped>
.enroll_img {
  width: 200px;
  height: 200px;
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
