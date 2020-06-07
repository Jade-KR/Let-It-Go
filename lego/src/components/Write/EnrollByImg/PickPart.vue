<template>
  <div>
    <div class="lego_parts_container">
      <div
        class="lego_parts_box"
        v-for="(part, idx) in slicedParts"
        :key="idx"
        @click="onPickPart(part, idx)"
      >
        <img
          src="../../../assets/icons/no_img.jpg"
          alt="no_image"
          class="lego_part"
          v-if="part[2] === ''"
        />
        <img v-else :src="part[2]" alt="no image" class="lego_part" />
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
      parts: state => state.write.pickedParts,
      pickedReset: state => state.write.pickedReset
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
      this.resetPickedPartByImg();
    },
    pickedReset() {
      for (let i = 0; i < this.slicedParts.length; ++i) {
        var nonTarget = document.getElementById(`checked-${i}`);
        nonTarget.style.display = "";
      }
    }
  },
  methods: {
    ...mapActions("write", ["pickPartBytImg"]),
    ...mapMutations("write", ["resetPickedPartByImg"]),
    onPickPart(part, idx) {
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
        part: part,
        isHave: isHave
      };
      this.pickPartBytImg(params);
    }
  }
};
</script>

<style scoped>
.lego_parts_container {
  width: 100%;
  height: fit-content;
  margin: auto;
  display: flex;
  flex-flow: row wrap;
  justify-content: center;
  text-align: center;
}
.lego_parts_box {
  display: inline-block;
  width: 100px;
  height: 100px;
  border: 1px black solid;
  margin: 5px;
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
