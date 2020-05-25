<template>
  <div class="container">
    <div class="control_box">
      <AddParts @page="page=1">
        <button class="submit_btn" slot="click">
          <i class="fas fa-plus"></i>&nbsp;부품 추가
        </button>
      </AddParts>
      <button class="delete_all" @click="clean()">
        <i class="far fa-trash-alt"></i>&nbsp;모두 삭제
      </button>
    </div>
    <div class="whole_box">
      <div class="item" v-for="(part, idx) in userParts" :key="`image${idx}`">
        <ModifyParts
          :partId="part.part_id"
          :colorId="part.color_id"
          :quantity="part.quantity"
          :rgb="part.rgb"
          :page="page"
          @pageDown="page -= 1"
        >
          <div class="body_img_box" slot="click">
            <img
              class="body_img"
              :src="`${part.image}` === `` ? noImage : `${part.image}`"
              alt="photo"
            />
          </div>
        </ModifyParts>
        <div class="part_info">
          <p class="part_id">{{part.part_id}}</p>
          <div class="part_color_cnt_box">
            <div class="color" :style="`background-color: #${part.rgb}`"></div>
            <p class="part_quantity">* {{part.quantity}}</p>
          </div>
        </div>
      </div>
    </div>
    <v-layout justify-center>
      <v-flex xs8>
        <v-card-text>
          <v-pagination :length="partPageLength" v-model="page"></v-pagination>
        </v-card-text>
      </v-flex>
    </v-layout>
  </div>
</template>
<script>
import AddParts from "./AddParts";
import { mapActions, mapState } from "vuex";
import ModifyParts from "./ModifyPart";

export default {
  components: {
    AddParts,
    ModifyParts
  },
  async mounted() {
    this.getUserParts(1);
  },
  data() {
    return {
      parts: [],
      noImage: require("../../../assets/icons/no_img.jpg"),
      pageLength: 10,
      dialog: false,
      page: 1
    };
  },
  methods: {
    ...mapActions("Parts", ["getUserParts", "deleteAll"]),
    clean() {
      this.deleteAll();
    }
  },
  computed: {
    ...mapState("Parts", ["userParts", "partPageLength", "originalCnt", "page"])
  },
  watch: {
    page() {
      this.getUserParts(this.page);
    }
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
  height: fit-content;
  margin: 5px;
  border: rgb(205, 205, 228) 3px solid;
  position: relative;
  cursor: pointer;
}
.item:hover {
  border: rgb(166, 166, 184) 3px solid;
}
.body_img_box {
  width: 100%;
  height: 70%;
  background: rgb(231, 231, 240);
  position: relative;
  margin: 0;
  padding: 0;
}
.body_img_box > img {
  width: 100%;
  height: 90%;
  margin: 0;
  padding: 0;
  /* border-radius: 180%; */
}
.part_info {
  width: 100%;
  height: 30%;
  background: rgb(248, 248, 248);
  margin: 0;
  padding-bottom: 10px;
  /* transform: translateY(-10px); */
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
  margin: 0;
  margin-left: 5px;
}
.control_box {
  display: flex;
  justify-content: flex-end;
  width: 90%;
  margin: auto;
}
.submit_btn {
  background: lightblue;
  color: white;
  width: 120px;
  height: 30px;
  border-radius: 5%;
  margin-bottom: 10px;
}
.delete_all {
  background: red;
  color: white;
  width: 120px;
  height: 30px;
  border-radius: 5%;
  margin-bottom: 10px;
  margin-left: 10px;
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
.part_color_cnt_box {
  display: flex;
  justify-content: center;
  align-items: baseline;
}
</style>