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
          <h3 class="title">부품을 등록하세요!</h3>
          <div class="close">
            <i class="fas fa-times" @click="dialog = 0"></i>
          </div>
        </div>
        <div class="form_box">
          <div class="label_box">
            <p class="label_name">부품 ID</p>
          </div>
          <div class="input_box">
            <v-autocomplete
              v-model="partId"
              :loading="loading"
              :items="items"
              :search-input.sync="search"
              cache-items
              class="mx-4"
              flat
              hide-no-data
              hide-details
              label="부품 id를 입력하세요"
              solo-inverted
              background-color="rgb(216, 216, 216)"
            ></v-autocomplete>
          </div>
        </div>
        <div class="form_box">
          <div class="label_box">
            <p class="label_name">부품 색</p>
          </div>
          <div class="input_box">
            <v-col class="d-flex" cols="12" sm="6">
              <v-select :items="partColors" filled label="부품 색" dense v-model="partColor"></v-select>
            </v-col>
          </div>
        </div>
        <div class="form_box">
          <div class="label_box">
            <p class="label_name">수량</p>
          </div>
          <div class="input_box">
            <v-col cols="12" sm="6" md="3">
              <v-text-field label="Filled" filled type="number" v-model="quantity"></v-text-field>
            </v-col>
          </div>
        </div>
        <div class="form_box">
          <div class="label_box">
            <p class="label_name"></p>
          </div>
          <div class="input_box">
            <button class="plus_btn" @click="addBasket()">
              <i class="fas fa-plus"></i>&nbsp;부품 추가
            </button>
            <button class="submit_btn">완료</button>
          </div>
        </div>
        <h2 class="basket_title">부품 추가 리스트</h2>
        <div class="parts_basket">
          <div class="body_img_box" v-for="(item, idx) in basket" :key="item+idx">
            <img class="body_img" :src="item.img" alt />
            <p class="part_quantity">{{item.id}} * {{item.quantity}}</p>
          </div>
        </div>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
import LegoParts from "../../../../jsonData/LegoParts.json";
import LegoColors from "../../../../jsonData/LegoColors.json";
export default {
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
      console.log(this.basket);
    }
  }
};
</script>

<style scoped>
.menu_box {
  height: fit-content;
  border-top: rgb(94, 116, 122) 5px solid;
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
.title {
  flex-basis: 90%;
  margin: 0;
  margin-left: 10px;
  font-size: 20px;
  padding: 10px 0;
}
.close {
  flex-basis: 10%;
  text-align: center;
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
  height: 40%;
  display: flex;
  flex-flow: row wrap;
}
</style>