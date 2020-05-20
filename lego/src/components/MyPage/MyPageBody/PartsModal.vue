<template>
  <div class="text-center">
    <v-dialog v-model="dialog" width="800px" class="modal_box">
      <template v-slot:activator="{ on }">
        <div v-on="on">
          <slot name="click" />
        </div>
      </template>

      <v-card class="menu_box">
        <div class="title_box">
          <h3 class="title_name">부품을 등록하세요!</h3>
          <div class="search_menus">
            <button class="search_by_id" @click="currentState=0">Id로</button>
            <button class="search_by_img" @click="checkImg()">이미지로</button>
          </div>
          <div class="close">
            <i class="fas fa-times" @click="dialog = 0"></i>
          </div>
        </div>
        <SearchById v-if="currentState === 0"></SearchById>
        <SearchByImg v-if="currentState === 1"></SearchByImg>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
import LegoParts from "../../../../jsonData/LegoParts.json";
import LegoColors from "../../../../jsonData/LegoColors.json";
import SearchById from "./PartsModal/SearchById";
import SearchByImg from "./PartsModal/SearchByImg";
import { mapActions } from "vuex";

export default {
  components: {
    SearchById,
    SearchByImg
  },
  data() {
    return {
      dialog: false,
      loading: false,
      items: [],
      partImg: "",
      search: null,
      partId: null,
      partColor: null,
      quantity: 0,
      currentState: 0,
      partColors: LegoColors.rows.map(color => {
        return color[1];
      }),
      selectStyle: LegoColors.rows.map(color => {
        return color[2];
      }),
      states: LegoParts.rows.map(part => {
        return part[0];
      }),
      images: LegoParts.rows.map(part => {
        return part[2];
      }),
      basket: []
    };
  },
  watch: {
    partId(id) {
      let idx = this.states.indexOf(id);
      this.partImg = this.images[idx];
    },
    search(val) {
      val && val !== this.select && this.querySelections(val);
    }
  },
  methods: {
    ...mapActions("Parts", ["changeStep"]),
    querySelections(v) {
      this.loading = true;
      // Simulated ajax query
      setTimeout(() => {
        this.items = this.states.filter(e => {
          return (e || "").toLowerCase().indexOf((v || "").toLowerCase()) > -1;
        });
        this.loading = false;
      }, 500);
    },
    addBasket() {
      const idx = this.states.indexOf(this.partId);
      if (idx === -1 || this.quantity < 1) {
        return;
      }
      for (let i = 0; i < this.basket.length; i++) {
        if (this.basket[i].id === this.partId) {
          this.basket[i].quantity += Number(this.quantity);
          return;
        }
      }
      this.basket.push({
        id: this.partId,
        img: this.partImg,
        color: this.partColors,
        quantity: Number(this.quantity)
      });
    },
    checkImg() {
      this.currentState = 1;
      this.changeStep(0);
    }
  }
};
</script>

<style scoped>
.menu_box {
  height: fit-content;
}
.right_body_box {
  border-style: none;
}
.all_box {
  width: 100%;
  border-style: none;
}
.form_box {
  display: flex;
  width: 100%;
}
.label_box {
  width: 25%;
  text-align: right;
  padding-right: 32px;
  display: flex;
  justify-content: flex-end;
  font-weight: bold;
}
.label_name {
  padding-top: 7px;
}
.input_box {
  width: 75%;
  display: flex;
  justify-content: left;
}
.user_id {
  text-align: left;
  font-size: 26px;
  padding-top: 5px;
}
.text_box {
  padding: 0;
}
.submit_btn {
  background: rgb(122, 203, 230);
  color: white;
  width: 120px;
  height: 30px;
  border-radius: 5%;
  margin-bottom: 10px;
}
.plus_btn {
  background: lightblue;
  color: white;
  width: 120px;
  height: 30px;
  border-radius: 5%;
  margin-bottom: 10px;
}
.title_box {
  display: flex;
  align-items: baseline;
  border-bottom: silver 1px solid;
  margin-bottom: 20px;
}
.title_name {
  flex-basis: 45%;
  margin: 0;
  margin-left: 10px;
  font-size: 30px;
  padding: 10px 0;
}
.close {
  flex-basis: 10%;
  text-align: right;
  height: 100%;
}
.close > i {
  cursor: pointer;
}
.green_window {
  display: inline-block;
  width: 520px;
  height: 34px;
  border: 3px solid #a4d8d5;
  background: white;
}
.input_text {
  width: 500px;
  height: 21px;
  margin: 6px 0 0 9px;
  border: 0;
  line-height: 21px;
  font-weight: bold;
  font-size: 16px;
  outline: none;
}
.nothign {
  color: rgb(216, 216, 216);
}

.part_info {
  width: 100%;
  height: 44%;
  position: relative;
  background: rgb(248, 248, 248);
  margin: 0;
  padding: 0;
  bottom: 7px;
}
.part_id {
  margin: 0;
  text-align: center;
  font-size: 14px;
}
.part_quantity {
  margin: 0;
  text-align: center;
  font-size: 15px;
}
.parts_basket {
  display: flex;
  height: 100%;
}
.body_img_box {
  width: 100px;
  height: 130px;
  margin: 0;
  padding: 0;
  display: flex;
  flex-direction: column;
  border: 1px black solid;
}
.body_img_box > img {
  width: 100%;
  height: 60%;
  margin: 0;
  padding: 0;
}
.body_img_box > p {
  height: 45%;
  display: flex;
  flex-flow: row wrap;
}
.search_menus {
  display: flex;
  flex-basis: 40%;
}
.search_by_id {
  margin-right: 50px;
}
</style>