<template>
  <div>
    <div id="part_header">
      <div @click="changeCate('all')" id="all_parts">
        <i class="fas fa-exclamation icon"></i>
        전체 부품
        <button
          @click.stop="addParts()"
          class="plus"
          :disabled="partFlag === 'need'"
          v-if="isLogin === true"
        >
          <i class="fas fa-plus"></i>
        </button>
        <button
          @click.stop="minusParts()"
          class="minus"
          :disabled="partFlag === 'need'"
          v-if="isLogin === true"
        >
          <i class="fas fa-minus"></i>
        </button>
      </div>
      <div @click="changeCate('need')" id="need_parts">
        <i class="fas fa-question icon"></i>
        필요한 부품
        <button
          @click.stop="addParts()"
          class="plus"
          :disabled="partFlag === 'all'"
          v-if="isLogin === true"
        >
          <i class="fas fa-plus"></i>
        </button>
      </div>
    </div>
    <hr id="dived_line" />
    <div v-if="isAll === true && partFlag === 'need'" id="iHaveAll">
      모두 가지고 있습니다!
    </div>
    <div class="lego_parts_container">
      <div
        class="lego_parts_box"
        v-for="(part, i) in slicedParts"
        :key="`detailPart-${i}`"
      >
        <img
          src="../../../assets/icons/no_img.jpg"
          alt="no_image"
          class="lego_part"
          v-if="part[1] === ''"
        />
        <img v-else :src="part[1]" :alt="part[0]" class="lego_part" />
        <div class="part_info">
          <div class="part_id">
            <div style="margin-bottom: 5px;">
              {{ part[0] }}
            </div>
            <div style="display: flex;">
              <div
                :style="
                  `width: 50px; height: 20px; background-color: #${part[2]}; border-radius: 20px; margin-right: 10px;`
                "
              ></div>
              <div style="font-size: 18px; transform: translateY(-3px);">
                <b>{{ part[3] }}</b>
              </div>
            </div>
          </div>
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
    <!-- <div @click="addParts()" id="add_my_parts" v-if="isLogin === true">
      <div v-if="partFlag === 'all'">
        전체 부품 내 부품에 추가
      </div>
      <div v-else>
        필요 부품 내 부품에 추가
      </div>
    </div> -->
    <div id="excel_export" v-if="isLogin === true">
      <download-excel
        :data="json_data"
        :fields="json_fields"
        :name="`${setName}_all.xls`"
        v-if="partFlag === 'all'"
      >
        전체 부품 엑셀로 다운로드
      </download-excel>
      <download-excel
        :data="json_data"
        :fields="json_fields"
        :name="`${setName}_need.xls`"
        v-else
      >
        필요 부품 엑셀로 다운로드
      </download-excel>
    </div>
  </div>
</template>

<script>
import LegoSort from "../../../../jsonData/LegoSort.json";
import { mapState, mapActions } from "vuex";

export default {
  props: {
    parts: {
      type: Array
    },
    setName: {
      type: String,
      default: ""
    }
  },
  data() {
    return {
      page: 1,
      pageLength: 1,
      slicedParts: [],
      imageStore: [],
      colorList: LegoSort["colors"],
      partDict: LegoSort["parts"],
      allParts: [],
      haveParts: Object(),
      needParts: [],
      sortedParts: [],
      partFlag: "all",
      isAll: false,
      isLogin: false,
      preprocedParts: [],

      json_fields: {
        "part ID": "part_id",
        "part Name": "part_name",
        "part Image Url": "part_img_url",
        RGB: "color_rgb",
        Quantity: "quantity"
      },
      json_data: [
        {
          part_id: "",
          part_name: "",
          part_img_url: "",
          color_rgb: "",
          quantity: 0
        }
      ],
      json_meta: [
        [
          {
            key: "charset",
            value: "utf-8"
          }
        ]
      ]
    };
  },
  computed: {
    ...mapState({
      myparts: state => state.detail.myparts
    }),
    start: function() {
      return this.page - 1;
    }
  },
  watch: {
    partFlag() {
      this.page = 1;
      this.pageLength = 1;
      if (this.partFlag === "need") {
        this.sortedParts = this.needParts;
        this.pageLength = Math.ceil(this.sortedParts.length / 27);
        this.slicedParts = this.sortedParts.slice(
          this.start * 27,
          this.page * 27
        );
        this.json_data = this.sortedParts.map(e => ({
          part_id: e[0],
          part_name: e[4],
          part_img_url: e[1],
          color_rgb: e[2],
          quantity: e[3]
        }));
      } else {
        this.sortedParts = this.allParts;
        this.pageLength = Math.ceil(this.sortedParts.length / 27);
        this.slicedParts = this.sortedParts.slice(
          this.start * 27,
          this.page * 27
        );
        this.json_data = this.sortedParts.map(e => ({
          part_id: e[0],
          part_name: e[4],
          part_img_url: e[1],
          color_rgb: e[2],
          quantity: e[3]
        }));
      }
    },
    myparts() {
      if (this.myparts.length === 0) {
        this.needParts = this.allParts;
        return;
      }
      const tempSortedParts = Object();
      const checkList = Object();
      this.preprocedParts.forEach(e => {
        let part_id = e.part_id;
        let color_id = e.color_id;
        let quantity = e.quantity;
        let temp = Object();
        temp[color_id] = quantity;
        temp[part_id] = part_id;
        temp["color_id_for_sort"] = color_id;
        tempSortedParts[`${e.part_id}_${e.color_id}`] = temp;
        let temp2 = [];
        temp2.push([
          this.partDict[e.part_id][0],
          this.partDict[e.part_id][1],
          this.colorList[e.color_id],
          e.quantity,
          this.partDict[e.part_id][2],
          e.color_id
        ]);
        checkList[`${e.part_id}_${e.color_id}`] = temp2;
      });
      for (let i = 0; i < this.myparts.length; ++i) {
        if (
          tempSortedParts[
            `${this.myparts[i].part_id}_${this.myparts[i].color_id}`
          ]
        ) {
          if (
            tempSortedParts[
              `${this.myparts[i].part_id}_${this.myparts[i].color_id}`
            ][this.myparts[i].color_id]
          ) {
            let tempCnt = 0;
            if (
              tempSortedParts[
                `${this.myparts[i].part_id}_${this.myparts[i].color_id}`
              ][this.myparts[i].color_id] >= this.myparts[i].quantity
            ) {
              tempCnt = this.myparts[i].quantity;
            } else {
              tempCnt =
                tempSortedParts[
                  `${this.myparts[i].part_id}_${this.myparts[i].color_id}`
                ][this.myparts[i].color_id];
            }
            let temp = [];
            temp.push([
              this.partDict[
                tempSortedParts[
                  `${this.myparts[i].part_id}_${this.myparts[i].color_id}`
                ][this.myparts[i].part_id]
              ][0],
              this.partDict[
                tempSortedParts[
                  `${this.myparts[i].part_id}_${this.myparts[i].color_id}`
                ][this.myparts[i].part_id]
              ][1],
              this.colorList[
                tempSortedParts[
                  `${this.myparts[i].part_id}_${this.myparts[i].color_id}`
                ].color_id_for_sort
              ],
              tempCnt,
              this.partDict[
                tempSortedParts[
                  `${this.myparts[i].part_id}_${this.myparts[i].color_id}`
                ][this.myparts[i].part_id]
              ][2],
              tempSortedParts[
                `${this.myparts[i].part_id}_${this.myparts[i].color_id}`
              ].color_id_for_sort
            ]);
            this.haveParts[
              `${
                this.partDict[
                  tempSortedParts[
                    `${this.myparts[i].part_id}_${this.myparts[i].color_id}`
                  ][this.myparts[i].part_id]
                ][0]
              }_${
                tempSortedParts[
                  `${this.myparts[i].part_id}_${this.myparts[i].color_id}`
                ].color_id_for_sort
              }`
            ] = temp;
          }
        }
      }

      for (let part_id in this.haveParts) {
        if (checkList[part_id][0][3] === this.haveParts[part_id][0][3]) {
          delete checkList[part_id];
        } else if (checkList[part_id][0][3] > this.haveParts[part_id][0][3]) {
          checkList[part_id][0][3] =
            checkList[part_id][0][3] - this.haveParts[part_id][0][3];
        } else if (checkList[part_id][0][3] < this.haveParts[part_id][0][3]) {
          delete checkList[part_id];
        }
      }
      for (let part_id in checkList) {
        this.needParts.push(checkList[part_id][0]);
      }
      if (this.needParts.length === 0) {
        this.isAll = true;
      }
    },
    start() {
      this.slicedParts = [];
      setTimeout(() => {
        this.slicedParts = this.sortedParts.slice(
          this.start * 27,
          this.page * 27
        );
      }, 300);
    }
  },
  async mounted() {
    if (localStorage.getItem("token")) {
      this.isLogin = true;
    }
    await this.getUserPartsAll();
    const partsObj = Object();
    this.parts.forEach(e => {
      let temp = `${e.part_id}_${e.color_id}`;
      if (partsObj[temp]) {
        partsObj[temp]["quantity"] += e.quantity;
      } else {
        partsObj[temp] = {
          color_id: e.color_id,
          part_id: e.part_id,
          quantity: e.quantity
        };
      }
    });
    for (let i in partsObj) {
      this.preprocedParts.push(partsObj[i]);
    }
    this.preprocedParts.forEach(e => {
      this.allParts.push([
        this.partDict[e.part_id][0],
        this.partDict[e.part_id][1],
        this.colorList[e.color_id],
        e.quantity,
        this.partDict[e.part_id][2],
        e.color_id
      ]);
    });
    this.sortedParts = this.allParts;
    this.pageLength = Math.ceil(this.sortedParts.length / 27);
    this.slicedParts = this.sortedParts.slice(this.start * 27, this.page * 27);
    this.json_data = this.sortedParts.map(e => ({
      part_id: e[0],
      part_name: e[4],
      part_img_url: e[1],
      color_rgb: e[2],
      quantity: e[3]
    }));
    const target = document.getElementById("all_parts");
    target.style.fontSize = "20px";
    target.style.color = "black";
  },
  methods: {
    ...mapActions("detail", ["getUserPartsAll", "addMyParts"]),
    changeCate(value) {
      if (value === "need") {
        if (!localStorage.getItem("token")) {
          alert("로그인 후 사용해 주세요");
          return;
        }
        const target = document.getElementById("need_parts");
        const nonTarget = document.getElementById("all_parts");
        target.style.fontSize = "20px";
        target.style.color = "black";
        nonTarget.style.fontSize = "16px";
        nonTarget.style.color = "gray";
      } else {
        const nonTarget = document.getElementById("need_parts");
        const target = document.getElementById("all_parts");
        target.style.fontSize = "20px";
        target.style.color = "black";
        nonTarget.style.fontSize = "16px";
        nonTarget.style.color = "gray";
      }
      this.partFlag = value;
    },
    async addParts() {
      const params = {
        UpdateList: []
      };
      this.sortedParts.forEach(e => {
        params["UpdateList"].push({
          part_id: String(e[0]),
          color_id: Number(e[5]),
          qte: Number(e[3])
        });
      });
      const result = await this.addMyParts(params);
      if (result === "수정 완료") {
        alert("내 부품에 추가되었습니다.");
        location.reload();
      } else {
        alert("문제가 생겼습니다.");
      }
    },
    async minusParts() {
      const params = {
        UpdateList: []
      };
      this.sortedParts.forEach(e => {
        params["UpdateList"].push({
          part_id: String(e[0]),
          color_id: Number(e[5]),
          qte: -Number(e[3])
        });
      });
      const result = await this.addMyParts(params);
      if (result === "수정 완료") {
        alert("내 부품에서 삭제 되었습니다.");
        location.reload();
      } else {
        alert("문제가 생겼습니다.");
      }
    }
  }
};
</script>

<style scoped>
#part_header {
  /* margin-bottom: 10px; */
  text-align: center;
  transform: translateY(-15px);
  font-size: 16px;
  color: gray;
}
#dived_line {
  width: 80%;
  margin: auto;
  border: 1px dashed gold;
  margin-bottom: 15px;
}
#all_parts,
#need_parts {
  display: inline-block;
  cursor: pointer;
  padding: 5px;
  width: 50%;
}
.icon {
  margin-right: 5px;
}
#excel_export {
  float: right;
  transform: translateY(-55px);
  padding: 5px;
  background-color: green;
  color: white;
  cursor: pointer;
  /* border-radius: 10px; */
}
#add_my_parts {
  float: left;
  transform: translateY(-55px);
  padding: 5px;
  background-color: green;
  color: white;
  cursor: pointer;
}
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
  cursor: default;
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
  opacity: 0;
  color: white;
  transform: translateY(10px);
  transition: all 0.3s ease-in-out;
  padding: 25px 10px;
}
.lego_parts_box:hover .part_id {
  transform: translateY(0);
  opacity: 1;
  transition: all 0.3s ease-in-out;
}
.lego_parts_box:hover .lego_part {
  opacity: 0.5;
  transition: all 0.3s ease-in-out;
}
#iHaveAll {
  text-align: center;
  font-size: 24px;
  margin: 20px;
  font-weight: 700;
}
.plus {
  margin-left: 5px;
  background-color: gold;
  color: white;
  width: 30px;
  height: 30px;
  display: inline-block;
}
.plus:hover::after {
  content: "내 부품에 추가합니다.";
  color: gold;
  font-size: 18px;
  width: 200px;
  position: absolute;
  transform: translate(7px, -27px);
  border: 1px solid black;
  background-color: white;
  padding: 5px;
  font-weight: 600;
}
.plus:disabled {
  opacity: 0;
}
.minus {
  margin-left: 5px;
  background-color: red;
  color: white;
  width: 30px;
  height: 30px;
  display: inline-block;
}
.minus:hover::after {
  content: "내 부품에서 삭제합니다.";
  color: red;
  font-size: 18px;
  width: 220px;
  position: absolute;
  transform: translate(7px, -27px);
  border: 1px solid black;
  background-color: white;
  padding: 5px;
  font-weight: 600;
}
.minus:disabled {
  opacity: 0;
}
</style>
