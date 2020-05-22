<template>
  <div class="container">
    <div class="control_box">
      <PartsModal>
        <button class="submit_btn" slot="click">
          <i class="fas fa-plus"></i>&nbsp;부품 추가
        </button>
      </PartsModal>
    </div>
    <div class="whole_box">
      <div class="item" v-for="(part, idx) in userParts" :key="`image${idx}`">
        <div class="body_img_box">
          <img class="body_img" :src="`${part.image}` === `` ? noImage : `${part.image}`" alt="dd" />
        </div>
        <div class="part_info">
          <p class="part_id">{{part.part_id}}</p>
          <div class="info_box">
            <div class="color" :style="`background-color: #${part.rgb}`"></div>
            <p class="part_quantity">* {{part.quantity}}</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
import PartsModal from "./PartsModal";
import { mapActions, mapState } from "vuex";

export default {
  components: {
    PartsModal
  },
  async mounted() {
    this.getUserParts();
  },
  data() {
    return {
      parts: [],
      noImage: require("../../../assets/icons/no_img.jpg")
    };
  },
  methods: {
    ...mapActions("Parts", ["getUserParts"])
  },
  computed: {
    ...mapState("Parts", ["userParts"])
  }
};
</script>

<style scoped>
.whole_box {
  height: 100%;
  width: 100%;
  display: flex;
  flex-flow: row wrap;
  margin: auto;
  justify-content: center;
}
.item {
  width: 110px;
  height: 140px;
  margin: 5px;
  border: rgb(205, 205, 228) 3px solid;
}
.item:hover {
  border: rgb(166, 166, 184) 3px solid;
}
.body_img_box {
  width: 100%;
  height: 70%;
  background: black;
  position: relative;
  margin: 0;
  padding: 0;
}
.body_img_box > img {
  width: 100%;
  height: 100%;
  margin: 0;
  padding: 0;
  /* border-radius: 180%; */
}
.part_info {
  width: 100%;
  height: 30%;
  background: rgb(248, 248, 248);
  margin: 0;
  padding: 0;
}
.part_id {
  margin: 0;
  text-align: center;
  font-size: 14px;
}
.part_quantity {
  display: inline-block;
  text-align: center;
  font-size: 15px;
  margin-left: 5px;
}
.control_box {
  display: flex;
  justify-content: space-between;
}
.submit_btn {
  background: lightblue;
  color: white;
  width: 120px;
  height: 30px;
  border-radius: 5%;
  margin-bottom: 10px;
}
.color {
  display: inline-block;
  width: 25px;
  height: 15px;
  border-radius: 30%;
}
.info_box {
  display: flex;
  align-items: baseline;
  justify-content: center;
}
</style>