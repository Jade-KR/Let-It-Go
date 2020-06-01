<template>
  <div
    id="home_body"
    v-infinite-scroll="loadMore"
    infinite-scroll-disabled="loading"
    infinite-scroll-distance="10"
  >
    <div id="home_show">
      <div v-if="!isCate">
        <user-category>
          <span slot="userCategory" id="userCategory" />
        </user-category>
      </div>
      <div
        @click="styleCheck()"
        v-if="styleFlag === false"
        class="home_show_btn"
      >
        모아보기
      </div>
      <div v-else @click="styleCheck()" class="home_show_btn">크게보기</div>
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
          :images="model.images"
          :nickname="model.nickname"
          :name="model.name"
          :isLike="model.is_like"
          :styleFlag="styleFlag"
        />
      </div>
    </div>
  </div>
</template>

<script>
import HomeCard from "@/components/Home/HomeCard";
import UserCategory from "../components/Home/UserCategory";
import { mapState, mapActions, mapMutations } from "vuex";

export default {
  name: "Home",
  components: {
    HomeCard,
    UserCategory
  },
  data() {
    return {
      loading: true,
      styleFlag: false,
      isCate: true,
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
      page: state => state.home.modelPage,
      likePage: state => state.home.likeModelPage,
      recommendPage: state => state.home.recommendModelPage,
      isCategory: state => state.auth.isCategory
    })
  },
  watch: {
    async homeCate() {
      await this.resetModels();
      const params = {
        page: 1,
        append: false
      };
      if (this.homeCate === 1) {
        await this.getModels(params);
      } else if (this.homeCate === 2) {
        await this.getLikeModels(params);
      } else if (this.homeCate === 3) {
        await this.getRecommendModels(params);
      }
      this.loading = false;
    }
  },
  async mounted() {
    if (localStorage.getItem("categories") === "null") {
      await this.setCate();
      document.getElementById("userCategory").click();
    }
    const params = {
      page: 1,
      append: false
    };
    if (this.homeCate === 1) {
      await this.getModels(params);
    } else if (this.homeCate === 2) {
      await this.getLikeModels(params);
    } else if (this.homeCate === 3) {
      await this.getRecommendModels(params);
    }

    this.loading = false;
  },
  beforeDestroy() {
    this.resetModels();
  },
  methods: {
    ...mapActions("home", ["getModels", "getLikeModels", "getRecommendModels"]),
    ...mapMutations("home", ["resetModels"]),
    styleCheck() {
      if (this.styleFlag === false) {
        this.styleFlag = true;
      } else {
        this.styleFlag = false;
      }
    },
    async loadMore() {
      this.loading = true;
      const params = {
        append: true
      };
      if (this.homeCate === 1) {
        params["page"] = this.page;
        await this.getModels(params);
      } else if (this.homeCate === 2) {
        params["page"] = this.likePage;
        await this.getLikeModels(params);
      } else if (this.homeCate === 3) {
        params["page"] = this.recommendPage;
        await this.getRecommendModels(params);
      }
      setTimeout(() => {
        this.loading = false;
      }, 1000);
    },
    setCate() {
      this.isCate = false;
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
  top: 70px;
  float: right;
}
.home_show_btn {
  cursor: pointer;
  background-color: gold;
  line-height: 50px;
  color: white;
  font-weight: 600;
  font-size: 20px;
}
</style>
