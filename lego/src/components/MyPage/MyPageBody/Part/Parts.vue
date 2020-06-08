<template>
  <div
    v-infinite-scroll="loadMore"
    infinite-scroll-disabled="loading"
    infinite-scroll-distance="10"
  >
    <div class="container" v-if="userParts.length !== 0">
      <div class="part_box">
        <div class="search_box">
          <div id="search_bar">
            <v-autocomplete
              v-model="searchWords"
              :items="parts"
              hide-details
              placeholder="검색어를 입력해주세요."
              color="rgb(255, 215, 0)"
              background-color="white"
              item-text="name"
              item-value="id"
              multiple
            >
              <template v-slot:item="data">
                <div style="margin-right: 100px; width: 40px;">
                  {{ data.item.name }}
                </div>
                <div
                  :style="
                    `width: 60px; height: 20px; background-color: #${data.item.color}; border-radius: 15px; border: 0.2px solid gray;`
                  "
                ></div>
              </template>
            </v-autocomplete>
          </div>
          <button id="search_bar_btn" @click="onSearch()">검색!</button>
          <button id="search_bar_btn_reset" @click="onReset()">초기화</button>
        </div>
        <div class="control_box">
          <AddParts @close="added">
            <button class="submit_btn" slot="click">
              <i class="fas fa-plus"></i>&nbsp;부품 추가
            </button>
          </AddParts>
          <DeleteModal @deleteAll="clean()">
            <button class="delete_all" slot="click">
              <i class="far fa-trash-alt"></i>&nbsp;모두 삭제
            </button>
          </DeleteModal>
        </div>
      </div>
      <div class="whole_box" v-if="isSearch === false">
        <div class="item" v-for="(part, idx) in userParts" :key="`image${idx}`">
          <ModifyParts
            :partId="part.part_id"
            :colorId="part.color_id"
            :quantity="part.quantity"
            :rgb="part.rgb"
            :idx="idx"
            @update="changed"
          >
            <div class="item_box" slot="click">
              <div class="body_img_box">
                <img
                  class="body_img"
                  :src="`${part.image}` === `` ? noImage : `${part.image}`"
                  alt="photo"
                />
              </div>
              <div class="part_info">
                <p class="part_id">{{ part.part_id }}</p>
                <div class="part_color_cnt_box">
                  <div
                    class="color"
                    :style="`background-color: #${part.rgb}`"
                  ></div>
                  <p class="part_quantity">* {{ part.quantity }}</p>
                </div>
              </div>
            </div>
          </ModifyParts>
        </div>
      </div>
      <div class="whole_box" v-else>
        <div
          class="item"
          v-for="(part, idx) in searchedParts"
          :key="`searched${idx}`"
        >
          <ModifyParts
            :partId="part.part_id"
            :colorId="part.color_id"
            :quantity="part.quantity"
            :rgb="part.rgb"
            :idx="idx"
            @update="changed"
          >
            <div class="item_box" slot="click">
              <div class="body_img_box">
                <img
                  class="body_img"
                  :src="`${part.image}` === `` ? noImage : `${part.image}`"
                  alt="photo"
                />
              </div>
              <div class="part_info">
                <p class="part_id">{{ part.part_id }}</p>
                <div class="part_color_cnt_box">
                  <div
                    class="color"
                    :style="`background-color: #${part.rgb}`"
                  ></div>
                  <p class="part_quantity">* {{ part.quantity }}</p>
                </div>
              </div>
            </div>
          </ModifyParts>
        </div>
      </div>
    </div>
    <div v-else>
      <NoContentsPart @added="added"></NoContentsPart>
    </div>
  </div>
</template>
<script>
import AddParts from "./AddParts/AddParts";
import DeleteModal from "./DeleteModal";
import { mapActions, mapState } from "vuex";
import ModifyParts from "./ModifyPart";
import NoContentsPart from "./NoContentsPart";

export default {
  components: {
    AddParts,
    ModifyParts,
    DeleteModal,
    NoContentsPart
  },
  data() {
    return {
      parts: [],
      noImage: require("../../../../assets/icons/no_img.jpg"),
      pageLength: 10,
      dialog: false,
      loading: true,
      searchWords: "",
      searchObj: Object(),
      searchedParts: [],
      isSearch: false
    };
  },
  computed: {
    ...mapState({
      userParts: state => state.Parts.partList,
      page: state => state.Parts.partPage,
      stopScroll: state => state.Parts.stopScroll,
      userAllParts: state => state.Parts.userAllParts
    })
  },
  async mounted() {
    await this.getAllParts();
    this.userAllParts.forEach(e => {
      this.parts.push({
        id: `${e.part_id}_${e.color_id}`,
        name: e.part_id,
        color: e.rgb
      });
      this.searchObj[`${e.part_id}_${e.color_id}`] = e;
    });
    const params = {
      page: 1,
      append: false,
      id: this.$route.params.user_id
    };
    await this.resetStop();
    await this.getParts(params);
    if (this.stopScroll === true) {
      return;
    }
    this.loading = false;
  },
  methods: {
    ...mapActions("Parts", [
      "getParts",
      "resetStop",
      "updateParts",
      "getAllParts"
    ]),
    async loadMore() {
      this.loading = true;
      const params = {
        page: this.page,
        append: true,
        id: this.$route.params.user_id
      };
      await this.getParts(params);
      if (this.stopScroll === true) {
        return;
      }
      setTimeout(() => {
        this.loading = false;
      }, 1000);
    },
    async clean() {
      let info = [];
      this.userParts.forEach(item => {
        let tmp = {
          part_id: String(item.part_id),
          color_id: Number(item.color_id),
          qte: -Number(item.quantity)
        };
        info.push(tmp);
      });
      await this.updateParts({ UpdateList: info });
      this.added();
    },
    changed(params) {
      if (this.isSearch === false) {
        if (params.quantity <= 0) {
          this.userParts.splice(params.idx, 1);
        } else {
          this.userParts[params.idx]["quantity"] = params.quantity;
        }
      } else {
        if (params.quantity <= 0) {
          this.searchedParts.splice(params.idx, 1);
        } else {
          this.searchedParts[params.idx]["quantity"] = params.quantity;
        }
        for (let i in this.searchObj) {
          if (i === `${params.part_id}_${params.color_id}`) {
            delete this.searchObj[i];
          }
        }
      }
    },
    async added() {
      this.loading = true;
      await this.resetStop();
      const params = {
        page: 1,
        append: false,
        id: this.$route.params.user_id
      };
      await this.getParts(params);
      if (this.stopScroll === true) {
        return;
      }
      this.loading = false;
    },
    onSearch() {
      if (this.searchWords === "") {
        alert("검색어를 입력해 주세요");
        return;
      }
      this.loading = true;
      const temp = [];
      for (let id in this.searchObj) {
        for (let i = 0; i < this.searchWords.length; ++i) {
          if (id === this.searchWords[i]) {
            temp.push(this.searchObj[id]);
          }
        }
      }
      this.searchedParts = temp;
      this.isSearch = true;
    },
    async onReset() {
      window.scrollTo(0, 0);
      const params = {
        page: 1,
        append: false,
        id: this.$route.params.user_id
      };
      await this.resetStop();
      await this.getParts(params);
      this.isSearch = false;
      this.loading = false;
      this.searchWords = "";
    }
  }
};
</script>

<style scoped>
.whole_box {
  height: 100%;
  width: 95%;
  display: flex;
  flex-flow: row wrap;
  margin: auto;
  /* justify-content: center; */
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
  margin-right: 40px;
}
.submit_btn {
  background: rgb(120, 187, 209);
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
.search_box {
  width: 100%;
  margin: auto;
  margin-left: 40px;
  transform: translateY(-10px);
}
#search_bar {
  width: 250px;
  display: inline-block;
}
#search_bar_btn {
  background-color: rgb(120, 187, 209);
  color: white;
  font-weight: 600;
  padding: 5px;
  width: 60px;
  height: 34px;
  border-radius: 5%;
}
#search_bar_btn_reset {
  background-color: red;
  color: white;
  font-weight: 600;
  padding: 5px;
  width: 60px;
  height: 34px;
  border-radius: 5%;
}
.part_box {
  display: flex;
  margin-bottom: 20px;
}
@media screen and (max-width: 600px) {
  .container {
    padding: 5px;
  }
  .whole_box {
    margin: 0;
    width: 100%;
    margin-top: 10px;
  }
  .item {
    width: 32vw;
    margin: 0;
  }
  .control_box {
    display: none;
  }
  .part_box {
    display: inline-block;
    width: 100%;
    margin-bottom: 0;
  }
  .search_box {
    margin: 0px;
  }
  #search_bar {
    width: 60%;
  }
  #search_bar_btn {
    width: 20%;
  }
  #search_bar_btn_reset {
    width: 20%;
  }
}
</style>
