<template>
  <div id="write_box">
    <div id="progress_bar">
      <div id="progress_step1" @click="goStep(1)">1</div>
      <hr
        id="progress_dash12"
        :style="
          step === 2 || step === 3 ? activeBarStyle[1] : deactiveBarStyle[1]
        "
      />
      <div
        id="progress_step2"
        @click="goStep(2)"
        :style="
          step === 2 || step === 3 ? activeBarStyle[0] : deactiveBarStyle[0]
        "
      >
        2
      </div>
      <hr
        id="progress_dash23"
        :style="step === 3 ? activeBarStyle[1] : deactiveBarStyle[1]"
      />
      <div
        id="progress_step3"
        @click="goStep(3)"
        :style="step === 3 ? activeBarStyle[0] : deactiveBarStyle[0]"
      >
        3
      </div>
    </div>
    <div id="write_desc">
      당신의 작품을 공유해 보세요!
    </div>
    <hr id="write_divideline" />
    <div id="write_info">
      <write-imgs v-if="currentStep === 1"></write-imgs>
      <write-desc v-if="currentStep === 2"></write-desc>
      <write-part v-if="currentStep === 3"></write-part>
    </div>
  </div>
</template>

<script>
import WriteImgs from "../../components/Write/WriteImgs.vue";
import WriteDesc from "../../components/Write/WriteDesc.vue";
import WritePart from "../../components/Write/WritePart.vue";
import { mapState, mapMutations } from "vuex";

export default {
  components: {
    WriteImgs,
    WriteDesc,
    WritePart
  },
  data() {
    return {
      activeBarStyle: [
        {
          backgroundColor: "green",
          color: "white",
          cursor: "pointer"
        },
        {
          border: "1px solid green"
        }
      ],
      deactiveBarStyle: [
        {
          backgroundColor: "gold",
          color: "black",
          cursor: "default"
        },
        {
          border: "1px solid gold"
        }
      ]
    };
  },
  computed: {
    ...mapState({
      step: state => state.write.step,
      currentStep: state => state.write.currentStep
    })
  },
  mounted() {
    const step1 = document.getElementById("progress_step1");
    step1.style.cursor = "pointer";
  },
  methods: {
    ...mapMutations("write", ["setCurrentStep"]),
    goStep(idx) {
      if (this.currentStep >= idx || this.step >= idx) {
        this.setCurrentStep(idx);
      }
    }
  }
};
</script>

<style scoped>
#write_box {
  border: 3px solid gold;
  width: 850px;
  margin: auto;
  margin-top: 20px;
  padding: 20px;
}
#progress_bar {
  text-align: center;
  margin: 20px;
  margin-top: 0px;
}
#progress_step1,
#progress_step2,
#progress_step3 {
  display: inline-block;
  width: 30px;
  height: 30px;
  border-radius: 50%;
  background-color: gold;
  padding: 5px;
  text-align: center;
}
#progress_step1 {
  background-color: green;
  color: white;
}
#progress_dash12,
#progress_dash23 {
  display: inline-block;
  width: 150px;
  vertical-align: middle;
  border: 1px solid gold;
}
#write_desc {
  text-align: center;
  margin-bottom: 10px;
  font-size: 22px;
}
#write_divideline {
  width: 80%;
  margin: auto;
  border: 1px dashed gold;
}
#write_info {
  margin-top: 20px;
}
</style>
