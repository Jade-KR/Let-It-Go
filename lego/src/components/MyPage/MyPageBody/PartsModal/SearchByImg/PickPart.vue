<template>
  <div>
    <div class="lego_parts_container">
      <div
        class="lego_parts_box"
        v-for="(part, idx) in slicedParts"
        :key="idx"
        @click="goAddPart(part[0])"
      >
        <img
          :src="part[2] === '' ? 'https://upload.wikimedia.org/wikipedia/commons/thumb/a/ac/No_image_available.svg/1024px-No_image_available.svg.png' : part[2]"
          alt="no image"
          class="lego_part"
        />
        <div class="part_info">
          <p class="part_id">{{part[0]}}</p>
        </div>
      </div>
    </div>
    <v-layout justify-center>
      <v-flex xs8>
        <v-card-text>
          <v-pagination :length="pageLength" v-model="page"></v-pagination>
        </v-card-text>
      </v-flex>
    </v-layout>
  </div>
</template>

<script>
import { mapState, mapActions } from "vuex";
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
      parts: state => state.Parts.filtered
    }),
    start: function() {
      return this.page - 1;
    }
  },
  watch: {
    start() {
      this.slicedParts = this.parts.slice(this.start * 25, this.page * 25);
    }
  },
  methods: {
    ...mapActions("Parts", ["changeStep", "pickPart"]),
    goAddPart(id) {
      this.pickPart(id);
      this.changeStep(2);
    }
  }
};
</script>

<style scoped>
.lego_parts_container {
  width: 90%;
  height: fit-content;
  margin: auto;
  display: flex;
  flex-flow: row wrap;
  justify-content: center;
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
</style>