<template>
  <div
    id="home_body"
    v-infinite-scroll="loadMore"
    infinite-scroll-disabled="loading"
    infinite-scroll-distance="10"
  >
    <div id="home_show">
      <div
        @click="styleCheck()"
        v-if="styleFlag === false"
        class="home_show_btn"
      >
        모아보기
      </div>
      <div v-else @click="styleCheck()" class="home_show_btn">
        크게보기
      </div>
    </div>
    <div :style="styleFlag ? matrixWidth : instaWidth">
      <div
        class="home_card"
        v-for="(model, i) in models"
        :key="`model-${i}`"
        :style="styleFlag ? matrixStyle : instaStyle"
      >
        <home-card
          :idx="i"
          :id="model.id"
          :images="model.image"
          :nickname="model.nickname"
          :name="model.name"
          :styleFlag="styleFlag"
        />
      </div>
    </div>
  </div>
</template>

<script>
import HomeCard from "@/components/Home/HomeCard";
import { mapState, mapActions } from "vuex";

export default {
  name: "Home",
  components: {
    HomeCard
  },
  data() {
    return {
      loading: true,
      styleFlag: false,
      matrixWidth: {
        width: "70vw",
        margin: "auto",
        textAlign: "center"
      },
      instaWidth: {},
      matrixStyle: {
        border: "5px solid gold",
        width: "250px",
        display: "inline-block",
        margin: "30px",
        backgroundColor: "white"
      },
      instaStyle: {
        border: "5px solid gold",
        width: "614px",
        margin: "30px auto",
        backgroundColor: "white"
      }
    };
  },
  computed: {
    ...mapState({
      homeCate: state => state.home.homeCate,
      models: state => state.home.modelList,
      page: state => state.home.modelPage
    })
  },
  async mounted() {
    const params = {
      page: 1,
      append: false
    };
    await this.getModels(params);
    this.loading = false;
  },
  methods: {
    ...mapActions("home", ["getModels"]),
    styleCheck() {
      if (this.styleFlag === false) {
        this.styleFlag = true;
      } else {
        this.styleFlag = false;
      }
    },
    async loadMore() {
      // console.log(this.page);
      this.loading = true;
      const params = {
        name: this.models[this.models.length - 1]["id"],
        page: this.page,
        append: true
      };

      await this.getModels(params);
      setTimeout(() => {
        this.loading = false;
      }, 1000);
    }
  }
};
</script>

<style scoped>
#home_body {
  box-sizing: border-box;
  width: 100%;
}
#home_show {
  width: 120px;
  padding: 10px;
  text-align: center;
  position: sticky;
  top: 20px;
  float: right;
}
.home_show_btn {
  cursor: pointer;
  background-color: skyblue;
  line-height: 50px;
  color: white;
  font-weight: 600;
  font-size: 20px;
}
</style>
