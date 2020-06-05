<template>
  <div>
    <div class="lego_parts_container">
      <h2 class="lego_parts_title">부품을 선택하세요</h2>
      <div
        class="lego_parts_box"
        v-for="(part, idx) in slicedParts"
        :key="idx"
        @click="goAddPart(part[0], idx)"
      >
        <img
          :src="
            part[2] === ''
              ? 'https://upload.wikimedia.org/wikipedia/commons/thumb/a/ac/No_image_available.svg/1024px-No_image_available.svg.png'
              : part[2]
          "
          alt="no image"
          class="lego_part"
        />
        <div class="part_info">
          <p class="part_id">{{ part[0] }}</p>
        </div>
        <div class="part_info">
          <i class="fas fa-check checked" :id="`checked-${idx}`"></i>
        </div>
      </div>
    </div>
    <v-layout justify-center>
      <v-flex xs8>
        <v-card-text>
          <v-pagination
            :length="pageLength"
            v-model="page"
            color="rgb(255, 215, 0)"
          ></v-pagination>
        </v-card-text>
      </v-flex>
    </v-layout>
    <div class="modal_footer">
      <button class="before_btn" @click="back()">이전</button>
      <button class="after_btn" @click="next()">다음</button>
    </div>
  </div>
</template>

<script>
import { mapState, mapActions, mapMutations } from "vuex";
export default {
  data() {
    return {
      page: 1,
      pageLength: 1,
      slicedParts: [],
      imageStore: []
    };
  },
  mounted() {
    this.pageLength = Math.ceil(this.parts.length / 25);
    this.slicedParts = this.parts.slice(this.start * 25, this.page * 25);
  },
  computed: {
    ...mapState({
      parts: state => state.Parts.filtered,
      pickedPart: state => state.Parts.pickedPart
    }),
    start: function() {
      return this.page - 1;
    }
  },
  watch: {
    start() {
      this.slicedParts = [];
      setTimeout(() => {
        this.slicedParts = this.parts.slice(this.start * 25, this.page * 25);
      }, 300);
    },
    page() {
      this.resetPart();
    }
  },
  methods: {
    ...mapActions("Parts", ["changeStep", "pickPart"]),
    ...mapMutations("Parts", ["resetPart"]),
    goAddPart(id, idx) {
      var isHave = false;
      for (let i = 0; i < this.slicedParts.length; ++i) {
        if (i === idx) {
          const target = document.getElementById(`checked-${idx}`);
          if (target.style.display === "") {
            target.style.display = "block";
          } else {
            target.style.display = "";
            isHave = true;
          }
          continue;
        }
      }
      const params = {
        id: id,
        isHave: isHave
      };
      this.pickPart(params);
    },
    back() {
      this.changeStep("back");
    },
    next() {
      this.changeStep("next");
    }
  }
};
</script>

<style scoped>
.lego_parts_container {
  width: 90%;
  height: fit-content;
  margin: auto;
}
.lego_parts_title {
  width: fit-content;
  margin: auto;
  border-bottom: rgb(255, 194, 82) 2px dotted;
  margin-bottom: 10px;
}
.lego_parts_box {
  display: inline-block;
  width: 100px;
  height: 100px;
  border: 1px black solid;
  margin: 10px;
  position: relative;
  cursor: pointer;
  background: black;
}
.lego_part {
  width: 100%;
  height: 100%;
  opacity: 1;
}
.part_info {
  width: inherit;
  height: inherit;
  overflow: hidden;
  position: absolute;
  top: 0;
}
.part_id {
  margin: 0;
  overflow: hidden;
  width: 100%;
  line-height: 100px;
  opacity: 0;
  color: white;
  transform: translateY(10px);
  transition: all 0.3s ease-in-out;
}
.lego_parts_box:hover .part_id {
  transform: translateY(0);
  opacity: 1;
  transition: all 0.3s ease-in-out;
}
.lego_parts_box:hover .lego_part {
  opacity: 0.6;
  transition: all 0.3s ease-in-out;
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
.modal_footer {
  display: flex;
  justify-content: space-between;
}
.checked {
  display: none;
  font-size: 50px;
  color: white;
  background-color: rgba(0, 0, 0, 0.5);
  width: 100%;
  height: 100%;
  padding: 20px;
  z-index: 5;
}
</style>
