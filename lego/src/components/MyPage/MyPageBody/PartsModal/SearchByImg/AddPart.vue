<template>
  <div class="right_body_box">
    <div class="all_box">
      <div class="form_box">
        <div class="label_box">
          <p class="label_name">부품 ID</p>
        </div>
        <div class="input_box">
          <div class="outline">
            <input type="text" :placeholder="partId" disabled />
          </div>
        </div>
      </div>
      <div class="form_box">
        <div class="label_box">
          <p class="label_name">부품 색</p>
        </div>
        <div class="input_box">
          <select name id v-model="partColor">
            <option
              :value="info[1]"
              v-for="(info, idx) in legoColor"
              :key="`info${idx}`"
              :id="`color${idx}`"
            >{{info[1]}}</option>
          </select>
        </div>
      </div>
      <div class="form_box">
        <div class="label_box">
          <p class="label_name">수량</p>
        </div>
        <div class="input_box">
          <input type="number" step="1" min="0" v-model="quantity" />
        </div>
      </div>
      <div class="form_box">
        <div class="label_box"></div>
        <div class="input_box">
          <button class="submit_btn" @click="goBasket()">추가</button>
        </div>
      </div>
      <div class="addList">
        <div class="item_size_box" v-for="(item, idx) in basket" :key="`item${idx}`">
          <img :src="item.img" alt class="item" />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { mapState, mapActions } from "vuex";
export default {
  data() {
    return {
      quantity: 0,
      partColor: "Black"
    };
  },
  computed: {
    ...mapState({
      partId: state => state.Parts.pickedPart,
      legoColor: state => state.Parts.legoColor,
      basket: state => state.Parts.basket
    })
  },
  mounted() {
    for (let i = 0; i < this.legoColor.length; i++) {
      let target = document.querySelector(`#color${i}`);
      console.log(`#${this.legoColor[i][2]}`);
      target.style.color = `#${this.legoColor[i][2]}`;
    }
  },
  methods: {
    ...mapActions("Parts", ["addBasket"]),
    goBasket() {
      if (this.quantity < 1) {
        return;
      }
      let params = {
        id: this.partId,
        quantity: this.quantity
      };
      this.addBasket(params);
    }
  }
};
</script>

<style scoped>
.all_box {
  width: 90%;
  margin: auto;
}
.photo_box {
  display: flex;
  width: 100%;
  margin-top: 30px;
  margin-bottom: 20px;
}
.form_box {
  display: flex;
  width: 100%;
}
.label_box {
  width: 30%;
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
  width: 70%;
  display: flex;
  justify-content: left;
}
input,
textarea {
  width: 80%;
  height: 100%;
  border: silver 1px solid;
}
.photo_frame {
  width: 50px;
  height: 50px;
  display: flex;
  justify-content: right;
}
.photo {
  width: 100%;
  height: 100%;
  border-radius: 180%;
}
.user_id {
  text-align: left;
  font-size: 26px;
  padding-top: 5px;
}
.change_photo_btn {
  width: 100%;
  text-align: left;
  font-size: 13px;
  position: relative;
  bottom: 10px;
  color: rgb(0, 140, 255);
  font-weight: bold;
}
.text_box {
  padding: 0;
}
.submit_btn {
  background: lightblue;
  color: white;
  width: 120px;
  height: 30px;
  border-radius: 5%;
}
.outline {
  border: green 3px solid;
}
.outline > input {
  border: none;
}
.addList {
  width: 90%;
  margin: auto;
  display: flex;
  flex-flow: row wrap;
}
.item_size_box {
  width: 100px;
  height: 100px;
  border: 1px solid black;
}
.item {
  width: 100%;
  height: 100%;
}
</style>