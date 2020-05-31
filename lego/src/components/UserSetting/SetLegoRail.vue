<template>
  <div class="right_body_box">
    <h1 class="header">레고레일 분류 현황</h1>
    <button class="send_btn" @click="onSubmit()">내 부품에 넣기</button>
    <button class="delete_all_btn">모두 삭제</button>
    <div class="classified_list">
      <div v-for="(item, idx) in realList" :key="`item${idx}`">
        <ModifyPart
          :partId="item.part_id"
          :colorId="item.color_id"
          :quantity="item.quantity"
          :idx="idx"
          @changedInfo="change"
        >
          <div class="items_container" slot="click">
            <div class="img_box">
              <img :src="item.part_img" alt="noImage" class="part_img" />
            </div>
            <div class="part_info">
              <p class="lego_id">{{item.part_id}}</p>
              <div class="lego_color_cnt">
                <div class="lego_color" :style="`background-color: #${item.rgb}`"></div>
                <span class="lego_cnt">* {{item.quantity}}</span>
              </div>
            </div>
          </div>
        </ModifyPart>
      </div>
    </div>
  </div>
</template>

<script>
import LegoSort from "../../../jsonData/LegoSort.json";
import ModifyPart from "./SetLegoRail/ModifyPart";
import { mapActions } from "vuex";
export default {
  components: {
    ModifyPart
  },
  data() {
    return {
      mockList: [
        { part_id: 10057, color_id: 2, quantity: 3 },
        { part_id: 10058, color_id: 1, quantity: 3 },
        { part_id: 10057, color_id: 3, quantity: 3 },
        { part_id: 10058, color_id: 2, quantity: 3 }
      ],
      check: LegoSort,
      realList: [],
      dialog: false
    };
  },
  mounted() {
    let realList = [];
    this.mockList.forEach(item => {
      let tmp = {
        part_id: item.part_id,
        color_id: item.color_id,
        quantity: item.quantity,
        part_img: LegoSort.parts[item.part_id][1],
        rgb: LegoSort.colors[item.color_id]
      };
      realList.push(tmp);
    });
    this.realList = realList;
  },
  methods: {
    ...mapActions("Parts", ["updateParts"]),
    change(info) {
      this.realList.forEach((item, i) => {
        if (
          item.color_id === info.colorId &&
          item.part_id === info.partId &&
          i !== info.idx
        ) {
          item.quantity += info.quantity;
          this.realList.splice(info.idx, 1);
          this.dialog = false;
          return;
        } else {
          this.realList[info.idx]["color_id"] = info.colorId;
          this.realList[info.idx]["rgb"] = LegoSort.colors[info.colorId];
          this.realList[info.idx]["quantity"] = info.quantity;
        }
      });
      this.dialog = false;
    },
    async onSubmit() {
      const newBasket = [];
      this.realList.forEach(item => {
        let info = {
          part_id: item.part_id,
          color_id: Number(item.color_id),
          qte: Number(item.quantity)
        };
        newBasket.push(info);
      });
      const params = { UpdateList: newBasket };
      await this.updateParts(params);
      alert("부품이 등록되었습니다");
      this.$router.push("mypage/" + localStorage.getItem("pk"));
    }
  }
};
</script>

<style scoped>
.header {
  width: fit-content;
  margin: auto;
  border-bottom: 2px dotted rgb(157, 201, 216);
  margin-bottom: 20px;
}
.classified_list {
  width: 90%;
  margin: auto;
  height: 380px;
  overflow-y: scroll;
  display: flex;
  flex-flow: row wrap;
  justify-content: flex-start;
}
.img_box {
  width: 100%;
  height: 70%;
}
.items_container {
  display: inline-block;
  margin: 4px;
  width: 110px;
  height: 150px;
  cursor: pointer;
  border: rgb(205, 205, 228) 3px solid;
}
.items_container:hover {
  border: rgb(166, 166, 184) 3px solid;
}
.items {
  /* display: inline-block;
  margin: 4px;
  width: 110px;
  height: 150px;
  cursor: pointer;
  border: rgb(205, 205, 228) 3px solid; */
}
.items:hover {
  border: rgb(166, 166, 184) 3px solid;
}
.part_info {
  width: 100%;
  height: 30%;
  border-top: rgb(231, 231, 240) 3px solid;
}
.part_img {
  width: 100%;
  height: 100%;
}
.lego_id {
  margin: 0;
}
.lego_color_cnt {
  transform: translateY(-5px);
  display: flex;
  justify-content: center;
  align-items: baseline;
}
.lego_color {
  display: inline-block;
  width: 20px;
  height: 10px;
  border-radius: 15%;
}
.lego_cnt {
  margin-left: 10px;
}
.send_btn {
  background: rgb(125, 205, 231);
  color: white;
  width: 130px;
  height: 30px;
  border-radius: 5%;
}
.delete_all_btn {
  background: red;
  color: white;
  width: 130px;
  height: 30px;
  border-radius: 5%;
  margin-bottom: 20px;
  margin-left: 10px;
}
</style>