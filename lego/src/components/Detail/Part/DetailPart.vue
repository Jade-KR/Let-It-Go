<template>
  <div>
    <div id="excel_export">
      <download-excel
        :data="json_data"
        :fields="json_fields"
        :name="`${setName}.xls`"
      >
        엑셀로 다운로드
      </download-excel>
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
          <!-- <p class="part_id">{{ part[0] }}</p> -->
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
  </div>
</template>

<script>
import LegoSort from "../../../../jsonData/LegoSort.json";

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
      sortedParts: [],

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
  mounted() {
    this.parts.forEach(e => {
      this.sortedParts.push([
        this.partDict[e.part_id][0],
        this.partDict[e.part_id][1],
        this.colorList[e.color_id],
        e.quantity,
        this.partDict[e.part_id][2]
      ]);
    });

    this.pageLength = Math.ceil(this.sortedParts.length / 27);
    this.slicedParts = this.sortedParts.slice(this.start * 27, this.page * 27);
    this.json_data = this.sortedParts.map(e => ({
      part_id: e[0],
      part_name: e[4],
      part_img_url: e[1],
      color_rgb: e[2],
      quantity: e[3]
    }));
  },
  computed: {
    start: function() {
      return this.page - 1;
    }
  },
  watch: {
    start() {
      this.slicedParts = [];
      setTimeout(() => {
        this.slicedParts = this.sortedParts.slice(
          this.start * 27,
          this.page * 27
        );
      }, 300);
    }
  }
};
</script>

<style scoped>
#excel_export {
  float: right;
  transform: translateY(-12px);
  padding: 5px;
  background-color: green;
  color: white;
  cursor: pointer;
  /* border-radius: 10px; */
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
</style>
