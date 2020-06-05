<template>
  <div>
    <div>
      <div id="part_input">
        <div class="star">*</div>
        <v-autocomplete
          v-model="partIdx"
          :items="partList"
          filled
          color="rgb(255, 215, 0)"
          background-color="white"
          item-text="name"
          item-value="idx"
          hide-details
          label="부품"
          placeholder="부품을 골라주세요"
          multiple
        />
      </div>
      <div id="color_input">
        <div class="star">*</div>
        <v-autocomplete
          v-model="selectedColor"
          :items="partColor"
          filled
          chips
          color="rgb(255, 215, 0)"
          background-color="white"
          item-text="colorName"
          item-value="idx"
          hide-details
          label="색상"
          placeholder="색상을 골라주세요"
        >
          <template v-slot:selection="data">
            <v-chip
              v-bind="data.attrs"
              :input-value="data.selected"
              @click="data.select"
              color="white"
              style="height: 54px;"
            >
              <v-avatar left>
                <div
                  :style="
                    `background-color: #${data.item.colorRgb}; width: 100%; height: 100%;`
                  "
                ></div>
              </v-avatar>
              {{ data.item.colorName }}
            </v-chip>
          </template>
          <template v-slot:item="data">
            <template v-if="typeof data.item !== 'object'">
              <v-list-item-content v-text="data.item"></v-list-item-content>
            </template>
            <template v-else>
              <v-list-item-avatar>
                <div
                  :style="
                    `background-color: #${data.item.colorRgb}; width: 100%; height: 100%;`
                  "
                ></div>
              </v-list-item-avatar>
              <v-list-item-content>
                <v-list-item-title
                  v-html="data.item.colorName"
                ></v-list-item-title>
              </v-list-item-content>
            </template>
          </template>
        </v-autocomplete>
      </div>
      <div id="quan_input">
        <div class="star star2">*</div>
        <v-text-field
          label="수량"
          type="number"
          min="1"
          step="1"
          v-model="partQuantity"
          hide-details
          height="55px"
          color="rgb(255, 215, 0)"
          style="width: 100px; font-size: 24px;"
        ></v-text-field>
      </div>
      <input
        type="submit"
        value="부품 추가"
        id="enroll_btn"
        @click="addList()"
      />
    </div>

    <hr
      style="border: 1px solid gold; margin-bottom: 20px;"
      v-show="this.basket.length > 0"
    />

    <div class="enrolled_parts">
      <div
        v-for="(part, i) in basket"
        :key="`part-${i}`"
        class="enrolled_parts"
      >
        <div>
          <img
            src="../../../../../assets/icons/delete.png"
            alt="delete"
            class="delete_btn"
            @click="deleteItem(i)"
          />
        </div>
        <img
          :src="part.partImg"
          alt="enroll_img"
          class="enroll_img"
          v-if="part.partImg"
        />
        <img
          src="../../../../../assets/icons/no_img.jpg"
          alt="enroll_img"
          class="enroll_img"
          v-else
        />
        <div class="enrolled_desc">
          <div class="enrolled_text">
            <div class="enrolled_name">{{ part.partId }}</div>
            <div
              class="enrolled_color"
              :style="
                `width: 100%; height: 10px; background-color: #${part.rgb};`
              "
            ></div>
          </div>
          <div class="enrolled_quan">* {{ part.quantity }}</div>
        </div>
      </div>
    </div>
    <div class="modal_footer">
      <button class="before_btn no_show">
        안보이나
      </button>
      <div id="baske_cnt">
        <b style="color: green; font-size: 24px;">{{ basket.length }}</b
        >종류, 총 <b style="color: green; font-size: 24px;">{{ partQnt }}</b
        >개의 부품이 등록되었습니다.
      </div>
      <button class="after_btn" :disabled="!flag" @click="onSubmit()">
        부품 등록
      </button>
    </div>
  </div>
</template>

<script>
import LegoParts from "../../../../../../jsonData/LegoParts.json";
import LegoColors from "../../../../../../jsonData/LegoColors.json";
import { mapActions, mapState } from "vuex";

export default {
  data() {
    return {
      partList: LegoParts.rows.map((e, i) => {
        return {
          name: e[0] + " " + e[1],
          idx: i,
          img: e[2]
        };
      }),
      partQuantity: 0,
      partIdx: "",
      partColor: LegoColors.rows.map((color, i) => {
        return {
          colorName: color[1],
          colorRgb: color[2],
          colorId: color[0],
          idx: i
        };
      }),
      selectedColor: "",
      partQnt: 0
    };
  },
  computed: {
    ...mapState({
      basket: state => state.Parts.basket
    }),
    flag: function() {
      return this.basket.length > 0 ? true : false;
    }
  },
  watch: {
    basket() {
      for (let i = 0; i < this.basket.length; ++i) {
        this.partQnt += Number(this.basket[i]["quantity"]);
      }
    }
  },
  mounted() {
    for (let i = 0; i < this.basket.length; ++i) {
      this.partQnt += Number(this.basket[i]["quantity"]);
    }
  },
  methods: {
    ...mapActions("Parts", [
      "addBasket",
      "deleteBasket",
      "updateParts",
      "getUserParts"
    ]),
    addList() {
      if (
        this.partId === "" ||
        this.selectedColor === "" ||
        this.partQuantity <= 0
      ) {
        return alert("필수 정보를 입력해주세요.");
      }
      for (let i = 0; i < this.partIdx.length; ++i) {
        let partInfo = {
          partId: LegoParts.rows[this.partIdx[i]][0],
          partImg: LegoParts.rows[this.partIdx[i]][2],
          colorId: LegoColors.rows[this.selectedColor][0],
          rgb: LegoColors.rows[this.selectedColor][2],
          quantity: Number(this.partQuantity)
        };
        this.addBasket(partInfo);
      }
      this.partIdx = "";
    },
    deleteItem(idx) {
      this.deleteBasket(idx);
    },
    async onSubmit() {
      const newBasket = [];
      this.basket.forEach(item => {
        let info = {
          part_id: item.partId,
          color_id: Number(item.colorId),
          qte: Number(item.quantity)
        };
        newBasket.push(info);
      });
      const params = { UpdateList: newBasket };
      await this.updateParts(params);
      this.$emit("close");
    }
  }
};
</script>

<style scoped>
#part_input,
#color_input {
  margin-bottom: 20px;
}
#color_input,
#quan_input,
#enroll_btn {
  display: inline-block;
}
#color_input {
  width: 60%;
}
#quan_input {
  margin: 0 20px;
}
#enroll_btn {
  padding: 10px;
  background-color: gold;
  width: 20%;
}
.enroll_img {
  width: 100px;
  height: 100px;
}
.enrolled_parts {
  display: inline-block;
  margin: 0 5px 10px 5px;
}
.enrolled_desc {
  text-align: center;
  display: flex;
  width: 100px;
}
.enrolled_text {
  min-width: 50%;
  display: inline-block;
}
.enrolled_name {
  white-space: nowrap;
  overflow: hidden;
}
.enrolled_quan {
  margin-left: 5px;
  min-width: 50%;
  display: inline-block;
}
.star {
  position: absolute;
  transform: translateX(5px);
  color: red;
  z-index: 1;
}
.star2 {
  transform: translate(-8px, 5px);
}
.delete_btn {
  width: 20px;
  height: 20px;
  position: absolute;
  cursor: pointer;
}
.delete_btn:hover {
  background-color: rgba(255, 0, 0, 0.8);
  border-radius: 50%;
}
.modal_footer {
  display: flex;
  justify-content: space-between;
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
#baske_cnt {
  margin-top: 20px;
  display: inline-block;
  font-size: 20px;
}
.no_show {
  color: white;
  background-color: white;
  opacity: 0;
  cursor: default;
}
</style>
